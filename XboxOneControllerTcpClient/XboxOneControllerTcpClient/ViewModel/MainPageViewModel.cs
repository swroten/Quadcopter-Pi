using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Windows.Gaming.Input;
using Windows.UI.Core;
using XboxOneControllerTcpClient.Model;

namespace XboxOneControllerTcpClient.ViewModel
{
    public class MainPageViewModel : INotifyPropertyChanged
    {
        public MainPageViewModel()
        {
            // Set Gather Message Frequency (ms)
            _maxNumberOfPoints = 600;
            _gatherMessageFrequencyMs = 50;
            _frequencyOfChartUpdateMs = 500;
            _timeSinceLastChartUpdateMs = 0;
            _timeSinceLastServerUpdateMs = 0;
            _frequencyToUpdateServerWithNewFlighDataMs = 250;

            // Create Flight Data
            _flightData = new FlightData();

            // Create Rest Client
            _myRestClient = new MyRestClient();

            // Start Listening
            StartListening();
        }

        #region Get / Set

        public FlightData FlightData
        {
            get
            {
                return _flightData;
            }
            set
            {
                _flightData = value;
                OnPropertyChanged("FlightData");
                OnPropertyChanged("CommandedRoll");
                OnPropertyChanged("CommandedPitch");
                OnPropertyChanged("CommandedYaw");
                OnPropertyChanged("CommandedThrottle");
                OnPropertyChanged("ObservedRoll");
                OnPropertyChanged("ObservedPitch");
                OnPropertyChanged("ObservedYaw");
                OnPropertyChanged("ObservedThrottle");
            }
        }

        public double LeftThumbStickX
        {
            get
            {
                return _leftThumbStickX;
            }
            set
            {
                _leftThumbStickX = value;
                OnPropertyChanged("LeftThumbStickX");
            }
        }

        public double LeftThumbStickY
        {
            get
            {
                return _leftThumbStickY;
            }
            set
            {
                _leftThumbStickY = value;
                OnPropertyChanged("LeftThumbStickY");
            }
        }

        public double RightThumbStickX
        {
            get
            {
                return _rightThumbStickX;
            }
            set
            {
                _rightThumbStickX = value;
                OnPropertyChanged("RightThumbStickX");
            }
        }

        public double RightThumbStickY
        {
            get
            {
                return _rightThumbStickY;
            }
            set
            {
                _rightThumbStickY = value;
                OnPropertyChanged("RightThumbStickY");
            }
        }

        public double LeftTriggerValue
        {
            get
            {
                return _leftTriggerValue;
            }
            set
            {
                _leftTriggerValue = value;
                OnPropertyChanged("LeftTriggerValue");
            }
        }

        public double RightTriggerValue
        {
            get
            {
                return _rightTriggerValue;
            }
            set
            {
                _rightTriggerValue = value;
                OnPropertyChanged("RightTriggerValue");
            }
        }

        public double CommandedRoll
        {
            get
            {
                return _flightData.CommandedRoll;
            }
            set
            {
                _flightData.CommandedRoll = value;
                OnPropertyChanged("CommandedRoll");
            }
        }

        public double CommandedPitch
        {
            get
            {
                return _flightData.CommandedPitch;
            }
            set
            {
                _flightData.CommandedPitch = value;
                OnPropertyChanged("CommandedPitch");
            }
        }

        public double CommandedYaw
        {
            get
            {
                return _flightData.CommandedYaw;
            }
            set
            {
                _flightData.CommandedYaw = value;
                OnPropertyChanged("CommandedYaw");
            }
        }

        public double CommandedThrottle
        {
            get
            {
                return _flightData.CommandedThrottle;
            }
            set
            {
                _flightData.CommandedThrottle = value;
                OnPropertyChanged("CommandedThrottle");
            }
        }

        public double ObservedRoll
        {
            get
            {
                return _flightData.ObservedRoll;
            }
            set
            {
                _flightData.ObservedRoll = value;
                OnPropertyChanged("ObservedRoll");
            }
        }

        public double ObservedPitch
        {
            get
            {
                return _flightData.ObservedPitch;
            }
            set
            {
                _flightData.ObservedPitch = value;
                OnPropertyChanged("ObservedPitch");
            }
        }

        public double ObservedYaw
        {
            get
            {
                return _flightData.ObservedYaw;
            }
            set
            {
                _flightData.ObservedYaw = value;
                OnPropertyChanged("ObservedYaw");
            }
        }

        public double ObservedThrottle
        {
            get
            {
                return _flightData.ObservedThrottle;
            }
            set
            {
                _flightData.ObservedThrottle = value;
                OnPropertyChanged("ObservedThrottle");
            }
        }

        public ObservableCollection<DataPoint> ObservedRollDataPoints { get; } = new ObservableCollection<DataPoint>();

        public ObservableCollection<DataPoint> ObservedPitchDataPoints { get; } = new ObservableCollection<DataPoint>();

        public ObservableCollection<DataPoint> ObservedYawDataPoints { get; } = new ObservableCollection<DataPoint>();

        public ObservableCollection<DataPoint> ObservedThrottleDataPoints { get; } = new ObservableCollection<DataPoint>();

        public ObservableCollection<DataPoint> CommandedRollDataPoints { get; } = new ObservableCollection<DataPoint>();

        public ObservableCollection<DataPoint> CommandedPitchDataPoints { get; } = new ObservableCollection<DataPoint>();

        public ObservableCollection<DataPoint> CommandedYawDataPoints { get; } = new ObservableCollection<DataPoint>();

        public ObservableCollection<DataPoint> CommandedThrottleDataPoints { get; } = new ObservableCollection<DataPoint>();
        
        public ObservableCollection<Message> ReceivedCommands { get; } = new ObservableCollection<Message>();

        public static List<GamepadButtons> KnownGamepadButtons { get; } = new List<GamepadButtons>()
        {
            GamepadButtons.A,
            GamepadButtons.B,
            GamepadButtons.X,
            GamepadButtons.Y,
            GamepadButtons.Menu,
            GamepadButtons.DPadLeft,
            GamepadButtons.DPadRight,
            GamepadButtons.DPadUp,
            GamepadButtons.DPadDown,
            GamepadButtons.View,
            GamepadButtons.RightThumbstick,
            GamepadButtons.LeftThumbstick,
            GamepadButtons.LeftShoulder,
            GamepadButtons.RightShoulder
        };

        #endregion

        #region Business Logic

        private async void StartListening()
        {
            // Otherwise, start listening
            await Task.Run(async () =>
            {
                _isRunning = true;

                while (_isRunning)
                {
                    try
                    {
                        // Get the first controller
                        _controller = Gamepad.Gamepads.FirstOrDefault();

                        // Verify non-null
                        if (_controller != null)
                        {
                            // Process Command
                            await DispatchCommand(() => { ProcessCommand(_controller.GetCurrentReading()); });                            
                        }                        
                    }
                    catch (Exception ex)
                    {
                        string stop = ex.Message;
                    }

                    // New Messages Scanned for Every 
                    await Task.Delay(_gatherMessageFrequencyMs);
                }
            });
        }

        private void ProcessCommand(GamepadReading reading)
        {
            // Get Left Thumb Stick Values
            LeftThumbStickX = reading.LeftThumbstickX;
            LeftThumbStickY = reading.LeftThumbstickY;

            // Get Right Thumb Stick Values
            RightThumbStickX = reading.RightThumbstickX;
            RightThumbStickY = reading.RightThumbstickY;

            // Get Trigger Values
            LeftTriggerValue = reading.LeftTrigger;
            RightTriggerValue = reading.RightTrigger;

            // Step through each Known Gamepad Button and Determine if it is selected
            foreach (GamepadButtons button in KnownGamepadButtons)
            {
                // Check if Button Clicked
                if (reading.Buttons.HasFlag(button))
                {
                    // Send Message
                    ReceivedCommands.Insert(0, new Message($"Button '{button}' was Pressed..."));
                }
            }

            // Update Flight Data
            CommandedYaw = LeftThumbStickX;
            CommandedThrottle = LeftThumbStickY;
            CommandedRoll = RightThumbStickX;
            CommandedPitch = RightThumbStickY;

            // Accumulate time
            _timeSinceLastChartUpdateMs += _gatherMessageFrequencyMs;
            _timeSinceLastServerUpdateMs += _gatherMessageFrequencyMs;

            // Check if enough time has accumulated to post new data to Data Server
            if (_timeSinceLastServerUpdateMs > _frequencyToUpdateServerWithNewFlighDataMs)
            {
                // Reset Gather Time
                _timeSinceLastServerUpdateMs = 0;
                
                // Update Flight Data
                FlightData = _myRestClient.Update(_flightData).Result;

                // Test
                //ObservedPitch = FlightData.CommandedPitch;
                //ObservedRoll = FlightData.CommandedRoll;
                //ObservedThrottle = FlightData.CommandedThrottle;
                //ObservedYaw = FlightData.CommandedYaw;
            }

            // Check if enough time has accumlated to post a new data point to chart
            if (_timeSinceLastChartUpdateMs > _frequencyOfChartUpdateMs)
            {
                // Reset Gather Time
                _timeSinceLastChartUpdateMs = 0;

                // Add Data Points
                if (CommandedYawDataPoints.Count > _maxNumberOfPoints)
                {
                    // Remove First Commanded
                    CommandedYawDataPoints.RemoveAt(0);
                    CommandedThrottleDataPoints.RemoveAt(0);
                    CommandedRollDataPoints.RemoveAt(0);
                    CommandedPitchDataPoints.RemoveAt(0);

                    // Remove First Observed
                    ObservedYawDataPoints.RemoveAt(0);
                    ObservedThrottleDataPoints.RemoveAt(0);
                    ObservedRollDataPoints.RemoveAt(0);
                    ObservedPitchDataPoints.RemoveAt(0);
                }

                // Add New Commanded
                CommandedYawDataPoints.Add(new DataPoint() { Y = CommandedYaw });
                CommandedThrottleDataPoints.Add(new DataPoint() { Y = CommandedThrottle });
                CommandedRollDataPoints.Add(new DataPoint() { Y = CommandedRoll });
                CommandedPitchDataPoints.Add(new DataPoint() { Y = CommandedPitch });

                // Add New Observed
                ObservedYawDataPoints.Add(new DataPoint() { Y = ObservedYaw });
                ObservedThrottleDataPoints.Add(new DataPoint() { Y = ObservedThrottle });
                ObservedRollDataPoints.Add(new DataPoint() { Y = ObservedRoll });
                ObservedPitchDataPoints.Add(new DataPoint() { Y = ObservedPitch });
            }
        }
        
        private async Task DispatchCommand(DispatchedHandler handler)
        {
            await Windows.ApplicationModel.Core.CoreApplication.MainView.CoreWindow.Dispatcher.RunAsync(CoreDispatcherPriority.Normal, handler);
        }

        #endregion
        
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

        private bool _isRunning;
        private Gamepad _controller;
        private int _maxNumberOfPoints;
        private FlightData _flightData;
        private double _leftThumbStickX;
        private double _leftThumbStickY;
        private double _rightThumbStickX;
        private double _rightThumbStickY;
        private double _leftTriggerValue;
        private double _rightTriggerValue;
        private MyRestClient _myRestClient;
        private int _gatherMessageFrequencyMs;
        private int _frequencyOfChartUpdateMs;
        private int _timeSinceLastChartUpdateMs;
        private int _timeSinceLastServerUpdateMs;
        private int _frequencyToUpdateServerWithNewFlighDataMs;

    }
}
