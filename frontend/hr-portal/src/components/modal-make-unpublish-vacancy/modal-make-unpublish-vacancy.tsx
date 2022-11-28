import {useEffect, useState} from 'react';

import Modal from '../../reused-components/modal/modal';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {setStateUnpublishedVacancy} from '../../features/vacancy/vacancy-slice';
import './modal-make-unpublish-vacancy.scss';
import {getVacanciesForEmployer, patchStatusVacancyUnpublish} from '../../service/async-actions/async-actions-vacancy';

function ModalMakeUnpublishVacancy() {
  const isOpenUnpublishModalState = useAppSelector((state) => state.vacancy.isOpenUnpublishVacancyModal);
  const [isUnpublishModal, setIsUnpublishModal] = useState(isOpenUnpublishModalState);
  const vacancyID = useAppSelector((state) => state.vacancy.vacancyByID?.id);
  const isPublished = useAppSelector((state) => state.vacancy.isPublishedVacancy);
  const idDepartment = useAppSelector((state) => state.general.user?.department.id);
  const offset = useAppSelector((state) => state.vacancy.paramsForGetVacancies.offset);
  const dispatch = useAppDispatch();

  useEffect(() => {
    setIsUnpublishModal(isOpenUnpublishModalState);
  }, [isOpenUnpublishModalState]);

  useEffect(() => {
    dispatch(setStateUnpublishedVacancy(isUnpublishModal));
  }, [isUnpublishModal]);

  const handleClickUnpublishVacancy = () => {
    if (vacancyID) {
      dispatch(patchStatusVacancyUnpublish(vacancyID)).then(() => {
        if (idDepartment) {
          dispatch(getVacanciesForEmployer({isPublished, idDepartment, offset}));
        }
      });
      setIsUnpublishModal(false);
    }
  };

  const handleClickCancelAction = () => {
    setIsUnpublishModal(false);
  };

  return (
    <Modal
      padding="80px 80px 60px 80px"
      width={858}
      active={isUnpublishModal}
      setActive={setIsUnpublishModal}
    >
      <div className="element-publish-modal element-publish-modal__title">
        Вы уверены, что хотите снять вакансию с публикации?
      </div>
      <div className="element-publish-modal element-publish-modal__explanatoryText">
        Соискатели не смогут просматривать и откликаться на вакансию.
      </div>
      <div className="element-publish-modal element-publish-modal__actionBtn">
        <button className="btn-item" onClick={handleClickCancelAction}>
          Отмена
        </button>
        <button className="btn-item btn-item__general-action" onClick={handleClickUnpublishVacancy}>
          Снять с публикации
        </button>
      </div>
    </Modal>
  );
}

export default ModalMakeUnpublishVacancy;