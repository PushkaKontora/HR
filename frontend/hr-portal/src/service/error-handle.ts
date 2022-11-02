import {resetError, setError} from '../features/general/general-slice';
import {useAppDispatch} from '../app/hooks';

export const processErrorHandle = (message: string): void => {
  const dispatch = useAppDispatch();
  dispatch(setError(message));
  dispatch(resetError());
};
