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

        public int Id
        {
            get
            {
                return _id;
            }
            set
            {
                _id = value;
            }
        }

        public double Roll
        {
            get
            {
                return _roll;
            }
            set
            {
                _roll = ScaleAngle(value);
            }
        }

        public double Pitch
        {
            get
            {
                return _pitch;
            }
            set
            {
                _pitch = ScaleAngle(value);
            }
        }

        public double Yaw
        {
            get
            {
                return _yaw;
            }
            set
            {
                _yaw = ScaleAngle(value);
            }
        }

        public double Throttle
        {
            get
            {
                return _throttle;
            }
            set
            {
                // Scale between -1 and 1 to prevent garbage data transmission
                _throttle = Math.Min(1.0, Math.Max(-1.0, value));
            }
        }

        #endregion

        #region Business Logic

        private static double ScaleAngle(double angle)
        {
            return Math.Min(1.0, Math.Max(-1.0, Scale(angle, 0.0, 360.0, -1.0, 1.0)));
        }

        private static double Scale(double valueIn, double baseMin, double baseMax, double limitMin, double limitMax)
        {
            return (limitMin + (((valueIn - baseMin) * (limitMax - limitMin)) / (baseMax - baseMin)));
        }

        #endregion

        private int _id = 0;
        private double _roll = 0.0;
        private double _pitch = 0.0;
        private double _yaw = 0.0;
        private double _throttle = 0.0;

    }
}
