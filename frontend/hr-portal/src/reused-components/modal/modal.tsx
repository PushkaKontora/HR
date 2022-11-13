import React, {Dispatch, SetStateAction} from 'react';
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