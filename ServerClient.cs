using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net.Sockets;
using System.Threading;

namespace ServerEngine
{
    enum MudraProtocol { World, Chat, Inventory, Sound };

    public partial class ServerClient
    {
        protected Server Host;
        Socket s;
        Thread t;
        public string IPAddress;

        public delegate void ServerCommandFunction(List<string> message);

        protected Dictionary<string, ServerCommandFunction> ServerCommandActions = new Dictionary<string,ServerCommandFunction>();

        string WelcomeMsg = "0 Connection successful! This is our MOTD!\n"+
            "A note on Abilities: Once you gain an ability, you gain it forever and can use that command to interact with the world. To use it, just follow the syntax given when you gained it.\n"+
            "Please remember to, for the love of all that is keeping me from ripping your head off: USE THE NUMBER IDS FOR COMMANDS, NOT THE ACTUAL NAMES.\n";

        byte[] Buffer { get; set; }

        public ServerClient(Server host, Socket sock)
        {
            Host = host;
            s = sock;
            IPAddress = sock.LocalEndPoint.ToString().Split(':')[0];

            //Add server commands
            ServerCommandActions.Add("help", new ServerCommandFunction(HelpCommand));
            ServerCommandActions.Add("version", new ServerCommandFunction(VersionCommand));
        }

        ~ServerClient()
        {
            Console.WriteLine("Destructor was called.");
        }

        public void Run()
        {
            t = new Thread(new ThreadStart(this.Listener));
            t.IsBackground = true;
            t.Start();
        }

        public void SendRawMessage(string msg)
        {
            //Console.WriteLine("Sending '" + msg + "'"+" to "+this.IPAddress);
            byte[] data = Encoding.ASCII.GetBytes(msg);
            Array.Resize<byte>(ref data, s.SendBufferSize);
            s.Send(data);
        }

        public void SendChatMessage(string msg)
        {
            SendRawMessage(MudraProtocol.Chat.ToString("d") + " " + this.IPAddress + " " + msg);
        }

        public void SendWorldMessage(string msg)
        {
            if (msg != null)
            {
                string toSend = MudraProtocol.World.ToString("d") + " " + msg;
                SendRawMessage(toSend);
            }
        }

        protected virtual void OnSocketClose() { }

        public void Close()
        {
            s.Close();
            Console.WriteLine("Socket to " + IPAddress + " has been closed. Calling OnSocketClose()");
            this.OnSocketClose();
            Console.WriteLine("Cleaning client from server...");
            Host.RemoveClient(this);
        }

        public void Listener()
        {

            SendRawMessage(WelcomeMsg);
            Console.WriteLine("Listener for " + this.IPAddress + " has been started.");
            try
            {
                while (true)
                {

                    if (!s.Connected) { throw new SocketException(10054); }

                    Buffer = new byte[s.SendBufferSize];
                    int bytesRead = 0;

                    try
                    {
                        bytesRead = s.Receive(Buffer,s.SendBufferSize, SocketFlags.None);
                    }
                    catch(SocketException)
                    {
                        Console.WriteLine("Error on Receive(). Client probably disconnected. Will now Close().");
                        this.Close();
                        break;
                    }

                    if (bytesRead == 0)
                    {
                        Console.WriteLine("0 bytes read from client " + IPAddress + ". Closing client socket...");
                        this.Close();
                        break;
                    }


                    /** Format buffer to take care of whitespace or extra crap*/
                    List<byte> formatted = new List<byte>(bytesRead);
                    for (int i = 0; i < bytesRead; i++)
                    {
                        if (Buffer[i] != default(byte))
                        {
                            formatted.Add(Buffer[i]);
                        }
                    }

                    string strData = Encoding.ASCII.GetString(formatted.ToArray()).Trim();

                    if (string.IsNullOrWhiteSpace(strData)) continue;

                    Console.WriteLine(this.IPAddress + ": " +strData);

                    List<string> tokens = strData.Split(' ').ToList<string>();

                    if (ServerCommandActions.ContainsKey(tokens[0].ToLower()))
                    {
                        ServerCommandActions[tokens[0].ToLower()](tokens);
                    }
                }
            }
            catch (SocketException error)
            {
                Console.WriteLine(error.ToString());
            }
        }
    }
}
