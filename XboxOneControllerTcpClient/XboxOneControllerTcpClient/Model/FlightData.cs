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

        public double CommandedRoll
        {
            get
            {
                return _commandedRoll;
            }
            set
            {
                // Scale between -1 and 1 to prevent garbage data transmission
                _commandedRoll = Math.Min(1.0, Math.Max(-1.0, value));
            }
        }

        public double CommandedPitch
        {
            get
            {
                return _commandedPitch;
            }
            set
            {
                // Scale between -1 and 1 to prevent garbage data transmission
                _commandedPitch = Math.Min(1.0, Math.Max(-1.0, value));
            }
        }

        public double CommandedYaw
        {
            get
            {
                return _commandedYaw;
            }
            set
            {
                // Scale between -1 and 1 to prevent garbage data transmission
                _commandedYaw = Math.Min(1.0, Math.Max(-1.0, value));
            }
        }

        public double CommandedThrottle
        {
            get
            {
                return _commandedThrottle;
            }
            set
            {
                // Scale between -1 and 1 to prevent garbage data transmission
                _commandedThrottle = Math.Min(1.0, Math.Max(-1.0, value));
            }
        }

        public double ObservedRoll
        {
            get
            {
                return _observedRoll;
            }
            set
            {
                // Scale between -1 and 1 to prevent garbage data transmission
                _observedRoll = Math.Min(1.0, Math.Max(-1.0, value));
            }
        }

        public double ObservedPitch
        {
            get
            {
                return _observedPitch;
            }
            set
            {
                // Scale between -1 and 1 to prevent garbage data transmission
                _observedPitch = Math.Min(1.0, Math.Max(-1.0, value));
            }
        }

        public double ObservedYaw
        {
            get
            {
                return _observedYaw;
            }
            set
            {
                // Scale between -1 and 1 to prevent garbage data transmission
                _observedYaw = Math.Min(1.0, Math.Max(-1.0, value));
            }
        }

        public double ObservedThrottle
        {
            get
            {
                return _observedThrottle;
            }
            set
            {
                // Scale between -1 and 1 to prevent garbage data transmission
                _observedThrottle = Math.Min(1.0, Math.Max(-1.0, value));
            }
        }

        #endregion

        private double _commandedRoll = 0.0;
        private double _commandedPitch = 0.0;
        private double _commandedYaw = 0.0;
        private double _commandedThrottle = 0.0;
        private double _observedRoll = 0.0;
        private double _observedPitch = 0.0;
        private double _observedYaw = 0.0;
        private double _observedThrottle = 0.0;

    }
}
