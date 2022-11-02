import {useAppSelector} from '../../app/hooks';

function ErrorMessage(): JSX.Element | null {
  const error = useAppSelector((state) => state.general.error);

  return (error)
    ? <div className='error-message'>{error}</div>
    : null;

}

export default ErrorMessage;