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
        public double Kp
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
                        CommandedData.RollKp = value;
                        break;
                    case FlightStates.Pitch:
                        ObservedData.PitchKp = value;
                        CommandedData.PitchKp = value;
                        break;
                    case FlightStates.Yaw:
                        ObservedData.YawKp = value;
                        CommandedData.YawKp = value;
                        break;
                    case FlightStates.Throttle:
                        ObservedData.ThrottleKp = value;
                        CommandedData.ThrottleKp = value;
                        break;
                }
            }
        }
        public double Ki
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
                        CommandedData.RollKi = value;
                        break;
                    case FlightStates.Pitch:
                        ObservedData.PitchKi = value;
                        CommandedData.PitchKi = value;
                        break;
                    case FlightStates.Yaw:
                        ObservedData.YawKi = value;
                        CommandedData.YawKi = value;
                        break;
                    case FlightStates.Throttle:
                        ObservedData.ThrottleKi = value;
                        CommandedData.ThrottleKi = value;
                        break;
                }
            }
        }
        public double Kd
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
                        CommandedData.RollKd = value;
                        break;
                    case FlightStates.Pitch:
                        ObservedData.PitchKd = value;
                        CommandedData.PitchKd = value;
                        break;
                    case FlightStates.Yaw:
                        ObservedData.YawKd = value;
                        CommandedData.YawKd = value;
                        break;
                    case FlightStates.Throttle:
                        ObservedData.ThrottleKd = value;
                        CommandedData.ThrottleKd = value;
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
        public Commanded CommandedData { get; private set; }
        public Observed ObservedData { get; private set; }
        
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
            OnPropertyChanged("Kp");
            OnPropertyChanged("Ki");
            OnPropertyChanged("Kd");
            OnPropertyChanged("Error");
            OnPropertyChanged("State");
            OnPropertyChanged("CommandedData");
            OnPropertyChanged("ObservedData");
        }
    }
}
