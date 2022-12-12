import {ToastContainer} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import {useAppSelector} from '../../app/hooks';

export function ToastWrapper() {

  return (
    <ToastContainer
      position="bottom-right"
      autoClose={5000}
      limit={3}
      newestOnTop={false}
      closeOnClick
      rtl={false}
      pauseOnFocusLoss
      draggable
      toastStyle={{backgroundColor: '#242424', color: '#fff'}}
      theme="colored"/>
  );
}
