using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace XboxOneControllerTcpClient.Model
{
    public class Commanded
    {
        public Commanded()
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
                // Scale between -1 and 1 to prevent garbage data transmission
                _roll = Math.Min(1.0, Math.Max(-1.0, value));
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
                // Scale between -1 and 1 to prevent garbage data transmission
                _pitch = Math.Min(1.0, Math.Max(-1.0, value));
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
                // Scale between -1 and 1 to prevent garbage data transmission
                _yaw = Math.Min(1.0, Math.Max(-1.0, value));
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
        
        private int _id = 0;
        private double _roll = 0.0;
        private double _pitch = 0.0;
        private double _yaw = 0.0;
        private double _throttle = 0.0;
    }
}
