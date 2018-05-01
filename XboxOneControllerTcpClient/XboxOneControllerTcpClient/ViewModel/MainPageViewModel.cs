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
            FlightStateDataViewModels = new List<FlightStateDataViewModel>()
            {
                new FlightStateDataViewModel(FlightStates.Roll, _commandedData, _observedData) {  cKp = 0.0, cKi = 0.0, cKd = 0.0 },
                new FlightStateDataViewModel(FlightStates.Pitch, _commandedData, _observedData) { cKp = 0.0, cKi = 0.0, cKd = 0.0 },
                new FlightStateDataViewModel(FlightStates.Yaw, _commandedData, _observedData) { cKp = 0.0, cKi = 0.0, cKd = 0.0 },
                new FlightStateDataViewModel(FlightStates.Throttle, _commandedData, _observedData) { cKp = 0.1, cKi = 0.05, cKd = 0.0 }
            };

            // Set Initial PID Constants

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
                OnPropertyChanged("IsArmedStatus");
                OnPropertyChanged("FlightStateDataViewModels");
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
                OnPropertyChanged("ObservedArmed");
                OnPropertyChanged("CommandedArmed");
            }
        }

        public double LeftThumbStickX
        {
            get
            {
                return Math.Round((_leftThumbStickX), 2);
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
                return Math.Round((_leftThumbStickY), 2);
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
                return Math.Round((_rightThumbStickX), 2);
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
                return Math.Round((_rightThumbStickY), 2);
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

        public bool ObservedArmed
        {
            get
            {
                return _observedData.Armed;
            }
            set
            {
                _observedData.Armed = value;
                OnPropertyChanged("IsArmedStatus");
                OnPropertyChanged("ObservedArmed");
            }
        }

        public bool CommandedArmed
        {
            get
            {
                return _commandedData.Armed;
            }
            set
            {
                _commandedData.Armed = value;
                OnPropertyChanged("CommandedArmed");
            }
        }

        public string IsArmedStatus
        {
            get
            {
                return (ObservedArmed) ? "ARMED" : "OFF";
            }
        }

        public List<FlightStateDataViewModel> FlightStateDataViewModels
        {
            get
            {
                return _flightStateDataViewModels;
            }
            set
            {
                _flightStateDataViewModels = value;
                OnPropertyChanged("FlightStateDataViewModels");
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
            // Check if Exit has been Demanded            
            CommandedData.Exit = (reading.Buttons.HasFlag(GamepadButtons.Y) || (CommandedData.Exit));

            // Get Left Thumb Stick Values
            LeftThumbStickX = reading.LeftThumbstickX;
            LeftThumbStickY = reading.LeftThumbstickY;

            // Get Right Thumb Stick Values
            RightThumbStickX = reading.RightThumbstickX;
            RightThumbStickY = reading.RightThumbstickY;

            // Get Trigger Values
            LeftTriggerValue = reading.LeftTrigger;
            RightTriggerValue = reading.RightTrigger;
            
            // Update Commanded Flight Data
            // CommandedData.Yaw = LeftThumbStickX;
            // CommandedData.Throttle = LeftThumbStickY;
            // CommandedData.Roll = RightThumbStickX;
            // CommandedData.Pitch = RightThumbStickY;
                   
            // Disarm is B is Pressed and it is currently Armed
            if (reading.Buttons.HasFlag(GamepadButtons.B) && CommandedArmed)
            {
                CommandedArmed = false;
            }
            // Otherwise arm if A is Pressed and it is not currently armed
            else if (reading.Buttons.HasFlag(GamepadButtons.A) && !CommandedArmed)
            {
                CommandedArmed = true;
            }

            // Check if D-PAD Up / Down / Left / Right Selected
            if (reading.Buttons.HasFlag(GamepadButtons.DPadUp))
            {
                CommandedData.ThrottleTrim += 0.01;
            }
            else if (reading.Buttons.HasFlag(GamepadButtons.DPadDown))
            {
                CommandedData.ThrottleTrim -= 0.01;
            }
            else if (reading.Buttons.HasFlag(GamepadButtons.DPadLeft))
            {
                CommandedData.YawTrim -= 0.01;
            }
            else if (reading.Buttons.HasFlag(GamepadButtons.DPadRight))
            {
                CommandedData.YawTrim += 0.01;
            }

            if (reading.Buttons.HasFlag(GamepadButtons.LeftShoulder))
            {
                CommandedData.RollTrim -= 0.01;
            }
            else if (reading.Buttons.HasFlag(GamepadButtons.RightShoulder))
            {
                CommandedData.RollTrim += 0.01;
            }
            else if (LeftTriggerValue > 0)
            {
                CommandedData.PitchTrim -= 0.01;
            }
            else if (RightTriggerValue > 0)
            {
                CommandedData.PitchTrim += 0.01;
            }
            
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

            // Notify Update
            for (int i = 0; i < FlightStateDataViewModels.Count; i++)
            {
                // Update Reference
                FlightStateDataViewModels[i].ObservedData = ObservedData;

                // Notify of Update
                FlightStateDataViewModels[i].NotifyValuesChanged();
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
                CommandedYawDataPoints.Add(new DataPoint() { Y = CommandedData.Yaw });
                CommandedThrottleDataPoints.Add(new DataPoint() { Y = CommandedData.Throttle });
                CommandedRollDataPoints.Add(new DataPoint() { Y = CommandedData.Roll });
                CommandedPitchDataPoints.Add(new DataPoint() { Y = CommandedData.Pitch });

                // Add New Observed
                ObservedYawDataPoints.Add(new DataPoint() { Y = ObservedData.Yaw });
                ObservedThrottleDataPoints.Add(new DataPoint() { Y = ObservedData.Throttle });
                ObservedRollDataPoints.Add(new DataPoint() { Y = ObservedData.Roll });
                ObservedPitchDataPoints.Add(new DataPoint() { Y = ObservedData.Pitch });

                // Increment the number of Points added to Chart
                _numberOfPointsAddedToChart++;
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
        private int _gatherMessageFrequencyMs;
        private int _frequencyOfChartUpdateMs;
        private int _numberOfPointsAddedToChart;
        private int _timeSinceLastChartUpdateMs;
        private int _timeSinceLastServerUpdateMs;
        private int _frequencyToUpdateServerWithNewFlighDataMs;
        private List<FlightStateDataViewModel> _flightStateDataViewModels;
    }
}
