using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Windows.Gaming.Input;
using Windows.Storage;
using Windows.UI.Core;
using XboxOneControllerTcpClient.Model;

namespace XboxOneControllerTcpClient.ViewModel
{
    public class MainPageViewModel : INotifyPropertyChanged
    {
        public MainPageViewModel()
        {
            // Set Gather Message Frequency (ms)
            _maxNumberOfPoints = 100;
            _gatherMessageFrequencyMs = 50;
            _frequencyOfChartUpdateMs = 500;
            _numberOfPointsAddedToChart = 0;
            _timeSinceLastChartUpdateMs = 0;
            _timeSinceLastServerUpdateMs = 0;
            _frequencyToUpdateServerWithNewFlighDataMs = 250;

            // Create Flight Data
            _observedData = new Observed();
            _commandedData = new Commanded();

            // Create Rest Client
            _myRestClient = new MyRestClient();

            // Start Listening
            StartListening();
        }

        #region Get / Set

        public Observed ObservedData
        {
            get
            {
                return _observedData;
            }
            set
            {
                _observedData = value;
                OnPropertyChanged("ObservedData");
                OnPropertyChanged("ObservedRoll");
                OnPropertyChanged("ObservedPitch");
                OnPropertyChanged("ObservedYaw");
                OnPropertyChanged("ObservedThrottle");
                OnPropertyChanged("RawRoll");
                OnPropertyChanged("RawPitch");
                OnPropertyChanged("RawYaw");
                OnPropertyChanged("RawThrottle");
            }
        }

        public Commanded CommandedData
        {
            get
            {
                return _commandedData;
            }
            set
            {
                _commandedData = value;
                OnPropertyChanged("CommandedData");
                OnPropertyChanged("CommandedRoll");
                OnPropertyChanged("CommandedPitch");
                OnPropertyChanged("CommandedYaw");
                OnPropertyChanged("CommandedThrottle");
            }
        }

        public double LeftThumbStickX
        {
            get
            {
                return Math.Round((_leftThumbStickX - _tareLeftThumbStickX), 1);
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
                return Math.Round((_leftThumbStickY - _tareLeftThumbStickY), 1);
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
                return Math.Round((_rightThumbStickX - _tareRightThumbStickX), 1);
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
                return Math.Round((_rightThumbStickY - _tareRightThumbStickY), 1);
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
                return _commandedData.Roll;
            }
            set
            {
                _commandedData.Roll = value;
                OnPropertyChanged("CommandedRoll");
            }
        }

        public double CommandedPitch
        {
            get
            {
                return _commandedData.Pitch;
            }
            set
            {
                _commandedData.Pitch = value;
                OnPropertyChanged("CommandedPitch");
            }
        }

        public double CommandedYaw
        {
            get
            {
                return _commandedData.Yaw;
            }
            set
            {
                _commandedData.Yaw = value;
                OnPropertyChanged("CommandedYaw");
            }
        }

        public double CommandedThrottle
        {
            get
            {
                return _commandedData.Throttle;
            }
            set
            {
                _commandedData.Throttle = value;
                OnPropertyChanged("CommandedThrottle");
            }
        }

        public double ObservedRoll
        {
            get
            {
                return _observedData.Roll;
            }
            set
            {
                _observedData.Roll = value;
                OnPropertyChanged("ObservedRoll");
            }
        }

        public double ObservedPitch
        {
            get
            {
                return _observedData.Pitch;
            }
            set
            {
                _observedData.Pitch = value;
                OnPropertyChanged("ObservedPitch");
            }
        }

        public double ObservedYaw
        {
            get
            {
                return _observedData.Yaw;
            }
            set
            {
                _observedData.Yaw = value;
                OnPropertyChanged("ObservedYaw");
            }
        }

        public double ObservedThrottle
        {
            get
            {
                return _observedData.Throttle;
            }
            set
            {
                _observedData.Throttle = value;
                OnPropertyChanged("ObservedThrottle");
            }
        }
        
        public double RawRoll
        {
            get
            {
                return _observedData.RawRoll;
            }
        }

        public double RawPitch
        {
            get
            {
                return _observedData.RawPitch;
            }
        }

        public double RawYaw
        {
            get
            {
                return _observedData.RawYaw;
            }
        }

        public double RawThrottle
        {
            get
            {
                return _observedData.RawThrottle;
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

            // Use Start Button to Reset Chart
            if (reading.Buttons.HasFlag(GamepadButtons.Menu))
            {
                // Reset Number of Points Added
                _numberOfPointsAddedToChart = 0;

                // Reset All Commanded
                CommandedYawDataPoints.Clear();
                CommandedRollDataPoints.Clear();
                CommandedPitchDataPoints.Clear();
                CommandedThrottleDataPoints.Clear();

                // Reset All Observed
                ObservedYawDataPoints.Clear();
                ObservedRollDataPoints.Clear();
                ObservedPitchDataPoints.Clear();
                ObservedThrottleDataPoints.Clear();
            }

            // Use View Button Print all Recorded values to CSV File
            if (reading.Buttons.HasFlag(GamepadButtons.View) && (!_isPrinting))
            {
                // Print data
                PrintData();
            }

            // Update Commanded Flight Data
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
                ObservedData = _myRestClient.Update(_observedData, _commandedData).Result;
            }

            // Check if enough time has accumlated to post a new data point to chart
            if (_timeSinceLastChartUpdateMs > _frequencyOfChartUpdateMs)
            {
                // Reset Gather Time
                _timeSinceLastChartUpdateMs = 0;

                // Add Data Points
                if (_numberOfPointsAddedToChart > _maxNumberOfPoints)
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

                // Increment the number of Points added to Chart
                _numberOfPointsAddedToChart++;
            }
        }
        
        private async void PrintData()
        {
            // Set True
            _isPrinting = true;

            try
            {
                // Create CSV String of Yaw Readings
                string yawReadingResults = string.Join(System.Environment.NewLine, ObservedYawDataPoints.Select(s => $"{s.X},{s.Y}")?.ToList() ?? new List<string>());
                string rollReadingResults = string.Join(System.Environment.NewLine, ObservedRollDataPoints.Select(s => $"{s.X},{s.Y}")?.ToList() ?? new List<string>());
                string pitchReadingResults = string.Join(System.Environment.NewLine, ObservedPitchDataPoints.Select(s => $"{s.X},{s.Y}")?.ToList() ?? new List<string>());

                // Get File Path
                StorageFolder storageFolder = ApplicationData.Current.LocalFolder;
                StorageFile yawFilePath = await storageFolder.CreateFileAsync($"yaw_{DateTime.Now.ToString("yyyyMMddHHmmss")}.csv",
                        CreationCollisionOption.ReplaceExisting);
                StorageFile rollFilePath = await storageFolder.CreateFileAsync($"roll_{DateTime.Now.ToString("yyyyMMddHHmmss")}.csv",
                        CreationCollisionOption.ReplaceExisting);
                StorageFile pitchFilePath = await storageFolder.CreateFileAsync($"pitch_{DateTime.Now.ToString("yyyyMMddHHmmss")}.csv",
                        CreationCollisionOption.ReplaceExisting);
                
                // Write all Data to CSV File
                await FileIO.WriteTextAsync(yawFilePath, yawReadingResults);
                await FileIO.WriteTextAsync(rollFilePath, rollReadingResults);
                await FileIO.WriteTextAsync(pitchFilePath, pitchReadingResults);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Failed to Print beause of '{ex.Message}'");
            }

            // Clear Printing Data Flag
            _isPrinting = false;
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
        private bool _isPrinting;
        private Gamepad _controller;
        private int _maxNumberOfPoints;
        private Observed _observedData;
        private Commanded _commandedData;
        private double _leftThumbStickX;
        private double _leftThumbStickY;
        private double _rightThumbStickX;
        private double _rightThumbStickY;
        private double _leftTriggerValue;
        private double _rightTriggerValue;
        private MyRestClient _myRestClient;
        private double _tareLeftThumbStickX;
        private double _tareLeftThumbStickY;
        private double _tareRightThumbStickX;
        private double _tareRightThumbStickY;
        private int _gatherMessageFrequencyMs;
        private int _frequencyOfChartUpdateMs;
        private int _numberOfPointsAddedToChart;
        private int _timeSinceLastChartUpdateMs;
        private int _timeSinceLastServerUpdateMs;
        private int _frequencyToUpdateServerWithNewFlighDataMs;

    }
}
