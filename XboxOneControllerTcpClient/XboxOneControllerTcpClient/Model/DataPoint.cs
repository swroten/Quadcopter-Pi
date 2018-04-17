using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace XboxOneControllerTcpClient.Model
{
    public class DataPoint
    {
        public DataPoint()
        {

        }

        public DateTime X { get; set; } = DateTime.UtcNow;
        public double Y { get; set; } = 0.0;

    }
}
