using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Net;
using System.Net.Sockets;
using System.Threading;

namespace ServerEngine
{
    public partial class Server
    {
        static Socket sck;
        public string buffer;
        public const string Version = "0.0.2";
        public List<ServerClient> Clients;

        int Port;

        public Server(int port)
        {
            Port = port;
        }

        public void RemoveClient(ServerClient victim)
        {
            Clients.Remove(victim);
        }

        public void WorldWorldMessage(string msg)
        {
            foreach (WorldOfMUDra.Player p in Clients)
            {
                p.SendWorldMessage(msg);
            }
        }

        public void WorldChatMessage(string user, string msg)
        {
            foreach (WorldOfMUDra.Player p in Clients)
            {
                p.SendChatMessage(user, msg);
            }
        }

        public void WorldChatMessage(string msg)
        {
            WorldChatMessage("Server", msg);
        }

        public void Start()
        {

            sck = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            sck.Bind(new IPEndPoint(0, Port));
            sck.Listen(100);

            Clients = new List<ServerClient>();
            //WorldOfMUDra.Globals.PassFile = new WorldOfMUDra.PasswordStorageFile("userpasses.txt");
            CreateWorld();

            while (true)
            {
                try
                {
                    Console.WriteLine("Waiting for clients...");
                    Clients.Add(new WorldOfMUDra.Player(this, sck.Accept()));
                    Console.WriteLine("Connection to " + Clients[Clients.Count - 1].IPAddress + " made. Now starting client thread...");
                    Clients[Clients.Count - 1].Run();
                    Console.WriteLine("Client thread started.");
                }
                catch (SocketException ex)
                {
                    Console.WriteLine(ex.ToString());
                }
            }
        }
    }
}
