import React, {useEffect, useState} from 'react';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {setStatePublishedVacancy, setStateUnpublishedVacancy} from '../../features/vacancy/vacancy-slice';
import {getVacanciesForEmployer, patchStatusVacancyPublish, patchStatusVacancyUnpublish} from '../../service/async-actions/async-actions-vacancy';
import Modal from '../../reused-components/modal/modal';

function ModalMakePublishVacancy() {
  const isOpenPublishVacancyModal = useAppSelector((state) => state.vacancy.isOpenPublishVacancyModal);
  const [isPublishModal, setIsPublishModal] = useState(isOpenPublishVacancyModal);
  const vacancyID = useAppSelector((state) => state.vacancy.vacancyByID?.id);
  const isPublished = useAppSelector((state) => state.vacancy.isPublishedVacancy);
  const idDepartment = useAppSelector((state) => state.general.user?.department.id);
  const offset = useAppSelector((state) => state.vacancy.paramsForGetVacancies.offset);
  const dispatch = useAppDispatch();

  useEffect(() => {
    setIsPublishModal(isOpenPublishVacancyModal);

  }, [isOpenPublishVacancyModal]);

  useEffect(() => {
    dispatch(setStatePublishedVacancy(isPublishModal));
  }, [isPublishModal]);

  const handleClickPublishVacancy = () => {
    if (vacancyID) {
      dispatch(patchStatusVacancyPublish(vacancyID)).then(() => {
        if (idDepartment) {
          dispatch(getVacanciesForEmployer({isPublished, idDepartment, offset}));
        }
      });
      setIsPublishModal(false);
    }
  };

  const handleClickCancelAction = () => {
    setIsPublishModal(false);
  };

  return (
    <Modal
      padding="80px 80px 60px 80px"
      width={786}
      active={isPublishModal}
      setActive={setIsPublishModal}
    >
      <div className="element-publish-modal element-publish-modal__title">
        Вы уверены, что хотите опубликовать вакансию?
      </div>
      <div className="element-publish-modal element-publish-modal__explanatoryText">
        Соискатели смогут просматривать и откликаться на вакансию.
      </div>
      <div className="element-publish-modal element-publish-modal__actionBtn">
        <button className="btn-item" onClick={handleClickCancelAction}>
          Отмена
        </button>
        <button className="btn-item btn-item__general-action" onClick={handleClickPublishVacancy}>
          Опубликовать
        </button>
      </div>
    </Modal>
  );
}

export default ModalMakePublishVacancy;