using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

using System.Runtime.InteropServices;

namespace ChangeVol
{

    class Program
    {
        private const int APPCOMMAND_VOLUME_MUTE = 0x80000;
        private const int WM_APPCOMMAND = 0x319;

        [DllImport("user32.dll")]
        public static extern IntPtr SendMessageW(IntPtr hWnd, int Msg, IntPtr wParam, IntPtr lParam);

        static void Main(string[] args)
        {
            Console.WriteLine("Started.");

            Console.WriteLine("Muting volume...");
            SendMessageW(Process.GetCurrentProcess().MainWindowHandle, WM_APPCOMMAND,
                Process.GetCurrentProcess().MainWindowHandle, (IntPtr) APPCOMMAND_VOLUME_MUTE);
            Console.WriteLine("Muted.");

            Console.ReadLine();

            Console.WriteLine("UnMuting volume...");
            SendMessageW(Process.GetCurrentProcess().MainWindowHandle, WM_APPCOMMAND,
                Process.GetCurrentProcess().MainWindowHandle, (IntPtr) APPCOMMAND_VOLUME_MUTE);
            Console.WriteLine("UnMuted.");
        }
    }
}
