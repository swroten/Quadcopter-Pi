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

        public double Roll
        {
            get
            {
                return ScaleRoll(RawRoll);
            }
            set
            {
                RawRoll = value;
            }
        }

        public double Pitch
        {
            get
            {
                return ScalePitch(RawPitch);
            }
            set
            {
                RawPitch = value;
            }
        }

        public double Yaw
        {
            get
            {
                return ScaleYaw(RawYaw);
            }
            set
            {
                RawYaw = value;
            }
        }

        public double Throttle
        {
            get
            {
                // Scale between -1 and 1 to prevent garbage data transmission
                return Math.Min(1.0, Math.Max(-1.0, RawThrottle));
            }
            set
            {
                RawThrottle = value;
            }
        }

        [JsonIgnore]
        public double RawRoll { get; private set; } = 0.0;

        [JsonIgnore]
        public double RawPitch { get; private set; } = 0.0;

        [JsonIgnore]
        public double RawYaw { get; private set; } = 0.0;

        [JsonIgnore]
        public double RawThrottle { get; private set; } = 0.0;

        #endregion

        #region Business Logic

        private static double ScaleYaw(double angle)
        {
            return Math.Min(1.0, Math.Max(-1.0, (((angle > 0) && (angle <= 180)) ?
                Scale(angle, 0.0, 180.0, 0, 1.0) :
                Scale(angle, 180.0, 360.0, -1.0, 0))));
        }

        private static double ScaleRoll(double angle)
        {
            return Scale(angle, -90.0, 90.0, -1.0, 1.0);
        }

        private static double ScalePitch(double angle)
        {
            return Scale(angle, -180.0, 180.0, -1.0, 1.0);
        }

        private static double Scale(double valueIn, double baseMin, double baseMax, double limitMin, double limitMax)
        {
            return (limitMin + (((valueIn - baseMin) * (limitMax - limitMin)) / (baseMax - baseMin)));
        }

        #endregion
    }
}
