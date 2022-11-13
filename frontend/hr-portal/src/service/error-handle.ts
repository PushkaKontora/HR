import {store} from '../app/store';
import {setError} from '../features/general/general-slice';
import {toast} from 'react-toastify';

export const processErrorHandle = (message: string): void => {
  store.dispatch(setError(message));
  toast.error(message);
  //dispatch(resetError());
};
