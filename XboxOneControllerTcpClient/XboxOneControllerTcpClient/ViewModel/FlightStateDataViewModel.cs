using System.ComponentModel;
using XboxOneControllerTcpClient.Model;

namespace XboxOneControllerTcpClient.ViewModel
{
    public class FlightStateDataViewModel : INotifyPropertyChanged
    {
        public FlightStateDataViewModel(FlightStates controlledState,
                                        Commanded commanded, 
                                        Observed observed)
        {
            State = controlledState;
            ObservedData = observed;
            CommandedData = commanded;
        }

        public double Commanded
        {
            get
            {
                // Initialize
                double commanded = 0.0;

                // Switch on State
                switch (State)
                {
                    case FlightStates.Roll:
                        commanded = CommandedData.Roll;
                        break;
                    case FlightStates.Pitch:
                        commanded = CommandedData.Pitch;
                        break;
                    case FlightStates.Yaw:
                        commanded = CommandedData.Yaw;
                        break;
                    case FlightStates.Throttle:
                        commanded = CommandedData.Throttle;
                        break;
                }

                // return
                return commanded;
            }
        }
        public double Observed
        {
            get
            {
                // Initialize
                double observed = 0.0;

                // Switch on State
                switch (State)
                {
                    case FlightStates.Roll:
                        observed = ObservedData.Roll;
                        break;
                    case FlightStates.Pitch:
                        observed = ObservedData.Pitch;
                        break;
                    case FlightStates.Yaw:
                        observed = ObservedData.Yaw;
                        break;
                    case FlightStates.Throttle:
                        observed = ObservedData.Throttle;
                        break;
                }

                // return
                return observed;
            }
        }
        public double cKp
        {
            get
            {
                // Initialize
                double kp = 0.0;

                // Switch on State
                switch (State)
                {
                    case FlightStates.Roll:
                        kp = CommandedData.RollKp;
                        break;
                    case FlightStates.Pitch:
                        kp = CommandedData.PitchKp;
                        break;
                    case FlightStates.Yaw:
                        kp = CommandedData.YawKp;
                        break;
                    case FlightStates.Throttle:
                        kp = CommandedData.ThrottleKp;
                        break;
                }

                // return
                return kp;
            }
            set
            {
                // Switch on State
                switch (State)
                {
                    case FlightStates.Roll:
                        CommandedData.RollKp = value;
                        break;
                    case FlightStates.Pitch:
                        CommandedData.PitchKp = value;
                        break;
                    case FlightStates.Yaw:
                        CommandedData.YawKp = value;
                        break;
                    case FlightStates.Throttle:
                        CommandedData.ThrottleKp = value;
                        break;
                }
                OnPropertyChanged("cKp");
            }
        }
        public double cKi
        {
            get
            {
                // Initialize
                double ki = 0.0;

                // Switch on State
                switch (State)
                {
                    case FlightStates.Roll:
                        ki = CommandedData.RollKi;
                        break;
                    case FlightStates.Pitch:
                        ki = CommandedData.PitchKi;
                        break;
                    case FlightStates.Yaw:
                        ki = CommandedData.YawKi;
                        break;
                    case FlightStates.Throttle:
                        ki = CommandedData.ThrottleKi;
                        break;
                }

                // return
                return ki;
            }
            set
            {
                // Switch on State
                switch (State)
                {
                    case FlightStates.Roll:
                        CommandedData.RollKi = value;
                        break;
                    case FlightStates.Pitch:
                        CommandedData.PitchKi = value;
                        break;
                    case FlightStates.Yaw:
                        CommandedData.YawKi = value;
                        break;
                    case FlightStates.Throttle:
                        CommandedData.ThrottleKi = value;
                        break;
                }
                OnPropertyChanged("cKi");
            }
        }
        public double cKd
        {
            get
            {
                // Initialize
                double kd = 0.0;

                // Switch on State
                switch (State)
                {
                    case FlightStates.Roll:
                        kd = CommandedData.RollKd;
                        break;
                    case FlightStates.Pitch:
                        kd = CommandedData.PitchKd;
                        break;
                    case FlightStates.Yaw:
                        kd = CommandedData.YawKd;
                        break;
                    case FlightStates.Throttle:
                        kd = CommandedData.ThrottleKd;
                        break;
                }

                // return
                return kd;
            }
            set
            {
                // Switch on State
                switch (State)
                {
                    case FlightStates.Roll:
                        CommandedData.RollKd = value;
                        break;
                    case FlightStates.Pitch:
                        CommandedData.PitchKd = value;
                        break;
                    case FlightStates.Yaw:
                        CommandedData.YawKd = value;
                        break;
                    case FlightStates.Throttle:
                        CommandedData.ThrottleKd = value;
                        break;
                }
                OnPropertyChanged("cKd");
            }
        }
        public double oKp
        {
            get
            {
                // Initialize
                double kp = 0.0;

                // Switch on State
                switch (State)
                {
                    case FlightStates.Roll:
                        kp = ObservedData.RollKp;
                        break;
                    case FlightStates.Pitch:
                        kp = ObservedData.PitchKp;
                        break;
                    case FlightStates.Yaw:
                        kp = ObservedData.YawKp;
                        break;
                    case FlightStates.Throttle:
                        kp = ObservedData.ThrottleKp;
                        break;
                }

                // return
                return kp;
            }
            set
            {
                // Switch on State
                switch (State)
                {
                    case FlightStates.Roll:
                        ObservedData.RollKp = value;
                        break;
                    case FlightStates.Pitch:
                        ObservedData.PitchKp = value;
                        break;
                    case FlightStates.Yaw:
                        ObservedData.YawKp = value;
                        break;
                    case FlightStates.Throttle:
                        ObservedData.ThrottleKp = value;
                        break;
                }
            }
        }
        public double oKi
        {
            get
            {
                // Initialize
                double ki = 0.0;

                // Switch on State
                switch (State)
                {
                    case FlightStates.Roll:
                        ki = ObservedData.RollKi;
                        break;
                    case FlightStates.Pitch:
                        ki = ObservedData.PitchKi;
                        break;
                    case FlightStates.Yaw:
                        ki = ObservedData.YawKi;
                        break;
                    case FlightStates.Throttle:
                        ki = ObservedData.ThrottleKi;
                        break;
                }

                // return
                return ki;
            }
            set
            {
                // Switch on State
                switch (State)
                {
                    case FlightStates.Roll:
                        ObservedData.RollKi = value;
                        break;
                    case FlightStates.Pitch:
                        ObservedData.PitchKi = value;
                        break;
                    case FlightStates.Yaw:
                        ObservedData.YawKi = value;
                        break;
                    case FlightStates.Throttle:
                        ObservedData.ThrottleKi = value;
                        break;
                }
            }
        }
        public double oKd
        {
            get
            {
                // Initialize
                double kd = 0.0;

                // Switch on State
                switch (State)
                {
                    case FlightStates.Roll:
                        kd = ObservedData.RollKd;
                        break;
                    case FlightStates.Pitch:
                        kd = ObservedData.PitchKd;
                        break;
                    case FlightStates.Yaw:
                        kd = ObservedData.YawKd;
                        break;
                    case FlightStates.Throttle:
                        kd = ObservedData.ThrottleKd;
                        break;
                }

                // return
                return kd;
            }
            set
            {
                // Switch on State
                switch (State)
                {
                    case FlightStates.Roll:
                        ObservedData.RollKd = value;
                        break;
                    case FlightStates.Pitch:
                        ObservedData.PitchKd = value;
                        break;
                    case FlightStates.Yaw:
                        ObservedData.YawKd = value;
                        break;
                    case FlightStates.Throttle:
                        ObservedData.ThrottleKd = value;
                        break;
                }
            }
        }
        public double Error
        {
            get
            {
                double error = 0.0;

                switch (State)
                {
                    case FlightStates.Roll:
                        error = ObservedData.RollError;
                        break;
                    case FlightStates.Pitch:
                        error = ObservedData.PitchError;
                        break;
                    case FlightStates.Yaw:
                        error = ObservedData.YawError;
                        break;
                    case FlightStates.Throttle:
                        error = ObservedData.ThrottleError;
                        break;
                }

                // return error
                return error;
            }
        }
        public FlightStates State { get; private set; }
        public Commanded CommandedData { get; set; }
        public Observed ObservedData { get; set; }
        
        #region INotifyPropertyChanged Members
        private void OnPropertyChanged(string propertyName)
        {
            if (PropertyChanged != null)
            {
                PropertyChanged(this, new PropertyChangedEventArgs(propertyName));
            }
        }
        #endregion

        public event PropertyChangedEventHandler PropertyChanged;

        public void NotifyValuesChanged()
        {
            OnPropertyChanged("Commanded");
            OnPropertyChanged("Observed");
            OnPropertyChanged("oKp");
            OnPropertyChanged("oKi");
            OnPropertyChanged("oKd");
            OnPropertyChanged("Error");
            OnPropertyChanged("State");
            OnPropertyChanged("CommandedData");
            OnPropertyChanged("ObservedData");
        }
    }
}
