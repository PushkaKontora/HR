import {ToastContainer} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import {useAppSelector} from '../../app/hooks';

export function ToastWrapper() {

  return (
    <ToastContainer
      position="bottom-right"
      autoClose={false}
      limit={3}
      newestOnTop={false}
      closeOnClick
      rtl={false}
      pauseOnFocusLoss
      draggable
      theme="colored"/>
  );
}
