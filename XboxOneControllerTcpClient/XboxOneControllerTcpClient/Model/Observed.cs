using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace XboxOneControllerTcpClient.Model
{
    public class Observed
    {
        public Observed()
        {

        }

        #region Get / Set

        public int Id { get; set; } = 0;

        public double Roll { get; set; } = 0.0;

        public double Pitch { get; set; } = 0.0;

        public double Yaw { get; set; } = 0.0;

        public double Throttle { get; set; } = 0.0;

        #endregion

    }
}
