using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using System.Threading;

namespace WPFConsole
{
    class Sound
    {
        WMPLib.WindowsMediaPlayer sound = new WMPLib.WindowsMediaPlayer();

        /// <summary>
        /// Constructor for sound class. Will check if file exists.
        /// </summary>
        /// <param name="filename">Name of the file to be played. MP3 prefered.</param>
        public Sound(string filename)
        {
            if (File.Exists(filename))
            {
                sound.URL = filename;
            }
        }

        /// <summary>
        /// If true, the sound will play forever on a loop.
        /// </summary>
        public bool Loop
        {
            set
            {
                if (value == true)
                {
                    sound.settings.setMode("loop", true);
                }
                else
                {
                    sound.settings.setMode("loop", false);
                }
            }
        }

        /// <summary>
        /// Play the sound.
        /// </summary>
        public void Play()
        {
            var t = new Thread(new ThreadStart(sound.controls.play));
            t.IsBackground = true;
            t.Start();
            //sound.controls.play();
        }

        /// <summary>
        /// Play the sound.
        /// </summary>
        /// <param name="loop">Decide whether the sound should be looped, or only played once.</param>
        public void Play(bool loop)
        {
            var t = new Thread(new ThreadStart(sound.controls.play));
            t.IsBackground = true;
            this.Loop = loop;
            t.Start();
            //sound.controls.play();
        }
    }
}
