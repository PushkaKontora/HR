import cl from 'classnames';
import React from 'react';

type ModalBtnStatusVacancyProps = {
  isPublishStatus: boolean,
  setIsPublishStatus: (value: boolean) => any
}

function ModalBtnStatusVacancy(props: ModalBtnStatusVacancyProps) {
  const {isPublishStatus, setIsPublishStatus} = props;
  return (
    <div className="toggleStatusVacancy">
      <button
        className={cl('btn-status', {'btn-status__active': isPublishStatus})}
        onClick={() => setIsPublishStatus(true)}
      >
        Активна
      </button>
      <button
        className={cl('btn-status', {'btn-status__active': !isPublishStatus})}
        onClick={() => setIsPublishStatus(false)}
      >
        Неактивна
      </button>
    </div>
  );
}

export default ModalBtnStatusVacancy;