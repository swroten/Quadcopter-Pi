namespace XboxOneControllerTcpClient.Model
{
    public class Observed
    {
        public Observed()
        {

        }

        #region Get / Set

        public int Id { get; set; } = 0;

        public bool Armed { get; set; } = false;

        public double Roll { get; set; } = 0.0;

        public double RollKp { get; set; } = 0.0;

        public double RollKi { get; set; } = 0.0;

        public double RollKd { get; set; } = 0.0;

        public double RollError { get; set; } = 0.0;

        public double Pitch { get; set; } = 0.0;

        public double PitchKp { get; set; } = 0.0;

        public double PitchKi { get; set; } = 0.0;

        public double PitchKd { get; set; } = 0.0;

        public double PitchError { get; set; } = 0.0;

        public double Yaw { get; set; } = 0.0;

        public double YawKp { get; set; } = 0.0;

        public double YawKi { get; set; } = 0.0;

        public double YawKd { get; set; } = 0.0;

        public double YawError { get; set; } = 0.0;

        public double Throttle { get; set; } = 0.0;

        public double ThrottleKp { get; set; } = 0.0;

        public double ThrottleKi { get; set; } = 0.0;

        public double ThrottleKd { get; set; } = 0.0;

        public double ThrottleError { get; set; } = 0.0;

        #endregion

    }
}
