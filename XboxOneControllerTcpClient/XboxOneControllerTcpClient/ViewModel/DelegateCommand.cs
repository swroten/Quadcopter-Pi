using System;

namespace XboxOneControllerTcpClient.ViewModel
{
    public class DelegateCommand<T> : System.Windows.Input.ICommand where T : class
    {
        public DelegateCommand(Action<T> execute) : this(execute,null)
        {

        }

        public DelegateCommand(Action<T> execute, Predicate<T> canExecute)
        {
            _execute = execute;
            _canExecute = canExecute;
        }

        public bool CanExecute(object parameter)
        {
            return (_canExecute == null) ? true : _canExecute((T)parameter);
        }

        public void Execute(object parameter)
        {
            _execute((T)parameter);
        }

        public void RaiseCanExecuteChanged()
        {
            if (CanExecuteChanged != null)
            {
                CanExecuteChanged(this, EventArgs.Empty);
            }
        }

        public event EventHandler CanExecuteChanged;

        private readonly Action<T> _execute;
        private readonly Predicate<T> _canExecute;
    }
}
