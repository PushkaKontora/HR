import React, {Dispatch, SetStateAction, useEffect} from 'react';
import './styles/modal.styles';
import './styles/modal-wrapper.styles.scss';
import {ModalContent} from './styles/modal.styles';
import CloseCrossImg from '../../../src/assets/img/modal/close-cross.svg';
import cl from 'classnames';

type ModalProps = {
  active: boolean,
  setActive: Dispatch<SetStateAction<boolean>>,
  width?: number,
  padding?: string
  children?: React.ReactNode
}

function Modal(props: ModalProps) {
  const {active, setActive, children, width, padding} = props;

  const body = document.body;

  useEffect(() => {
    if (active) {
      body.classList.add('disable-scroll');
    }
    return () => {
      body.classList.remove('disable-scroll');
    };
  }, [active]);


  return (
    <div className={cl('modal', {'modal__active': active})} onClick={() => setActive(false)}>
      <ModalContent width={width && width} padding={padding && padding} className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="imgCloseCross">
          <img src={CloseCrossImg} alt="Close Cross Img" onClick={() => setActive(false)}/>
        </div>
        {children}
      </ModalContent>
    </div>
  );
}

export default Modal;

//todo: заблокировать скроллпри прокрутке