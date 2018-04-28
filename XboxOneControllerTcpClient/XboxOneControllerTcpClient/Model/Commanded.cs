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

        public int Id { get; set; } = 0;

        public bool Armed { get; set; } = false;

        public bool Exit { get; set; } = false;

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

        public double RollKp { get; set; } = 0.0;

        public double RollKi { get; set; } = 0.0;

        public double RollKd { get; set; } = 0.0;

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

        public double PitchKp { get; set; } = 0.0;

        public double PitchKi { get; set; } = 0.0;

        public double PitchKd { get; set; } = 0.0;

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

        public double YawKp { get; set; } = 0.0;

        public double YawKi { get; set; } = 0.0;

        public double YawKd { get; set; } = 0.0;

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

        public double ThrottleKp { get; set; } = 0.0;

        public double ThrottleKi { get; set; } = 0.0;

        public double ThrottleKd { get; set; } = 0.0;

        #endregion
        private double _roll = 0.0;
        private double _pitch = 0.0;
        private double _yaw = 0.0;
        private double _throttle = 0.0;
    }
}
