using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace XboxOneControllerTcpClient.Model
{
    public class FlightData
    {
        public FlightData()
        {

        }

        #region Get / Set

        public double CommandedRoll { get; set; } = 0.0;

        public double CommandedPitch { get; set; } = 0.0;

        public double CommandedYaw { get; set; } = 0.0;

        public double CommandedThrottle { get; set; } = 0.0;

        public double ObservedRoll { get; set; } = 0.0;

        public double ObservedPitch { get; set; } = 0.0;

        public double ObservedYaw { get; set; } = 0.0;

        public double ObservedThrottle { get; set; } = 0.0;

        #endregion

    }
}
