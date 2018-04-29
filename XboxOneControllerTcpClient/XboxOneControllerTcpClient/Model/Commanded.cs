using Newtonsoft.Json;
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
                _roll = Math.Min(1.0, Math.Max(-1.0, (value + RollTrim)));
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
                _pitch = Math.Min(1.0, Math.Max(-1.0, (value + PitchTrim)));
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
                _yaw = Math.Min(1.0, Math.Max(-1.0, (value + YawTrim)));
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
                _throttle = Math.Min(1.0, Math.Max(-1.0, (value + ThrottleTrim)));
            }
        }

        public double ThrottleKp { get; set; } = 0.0;

        public double ThrottleKi { get; set; } = 0.0;

        public double ThrottleKd { get; set; } = 0.0;

        [JsonIgnore]
        public double YawTrim
        {
            get
            {
                return _yawTrim;
            }
            set
            {
                // Recall Current Yaw Value
                double curValue = (Yaw - _yawTrim);

                // Set New Yaw Trim
                _yawTrim = value;

                // Set new Yaw Value
                Yaw = curValue;
            }
        }

        [JsonIgnore]
        public double RollTrim
        {
            get
            {
                return _rollTrim;
            }
            set
            {
                // Recall Current Roll Value
                double curValue = (Roll - _rollTrim);

                // Set New Roll Trim
                _rollTrim = value;

                // Set new Roll Value
                Roll = curValue;
            }
        }

        [JsonIgnore]
        public double PitchTrim
        {
            get
            {
                return _pitchTrim;
            }
            set
            {
                // Recall Current Pitch Value
                double curValue = (Pitch - _pitchTrim);

                // Set New Pitch Trim
                _pitchTrim = value;

                // Set new Pitch Value
                Pitch = curValue;
            }
        }

        [JsonIgnore]
        public double ThrottleTrim
        {
            get
            {
                return _throttleTrim;
            }
            set
            {
                // Recall Current Throttle Value
                double curValue = (Throttle - _throttleTrim);

                // Set New Throttle Trim
                _throttleTrim = value;

                // Set new Throttle Value
                Throttle = curValue;
            }
        }

        #endregion

        private double _roll = 0.0;
        private double _pitch = 0.0;
        private double _yaw = 0.0;
        private double _throttle = 0.0;
        private double _rollTrim = 0.0;
        private double _pitchTrim = 0.0;
        private double _yawTrim = 0.0;
        private double _throttleTrim = 0.0;
    }
}
