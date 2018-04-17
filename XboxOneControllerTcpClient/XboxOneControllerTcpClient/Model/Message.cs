using System;

namespace XboxOneControllerTcpClient.Model
{
    public class Message
    {
        public Message(string message)
        {
            Text = message;
        }

        public string Text { get; set; }
        public DateTime Time { get; set; } = DateTime.UtcNow;        
    }
}
