import VacancyList from '../vacancy-list/vacancy-list';
import {useEffect} from 'react';
import {getVacanciesForEmployer} from '../../service/async-actions/async-actions-vacancy';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import ModalMakeUnpublishVacancy from '../modal-make-unpublish-vacancy/modal-make-unpublish-vacancy';
import ModalEditVacancy from '../modal-edit-vacancy/modal-edit-vacancy';
import ModalMakePublishVacancy from '../modal-make-publish-vacancy/modal-make-publish-vacancy';
import ModalCreateVacancy from '../modal-create-vacancy/modal-create-vacancy';

function VacancyListEmployerMyVacancy() {
  const isPublished = useAppSelector((state) => state.vacancy.isPublishedVacancy);
  const idDepartment = useAppSelector((state) => state.general.user?.department.id);
  const offset = useAppSelector((state) => state.vacancy.paramsForGetVacancies.offset);
  const dispatch = useAppDispatch();

  useEffect(() => {
    if (idDepartment) {
      dispatch(getVacanciesForEmployer({isPublished, idDepartment: idDepartment, offset}));
    }
  }, [isPublished, idDepartment]);

  return (
    <>
      <ModalEditVacancy/>
      <ModalCreateVacancy/>
      <ModalMakeUnpublishVacancy/>
      <ModalMakePublishVacancy/>
      <VacancyList/>
    </>
  );
}

export default VacancyListEmployerMyVacancy;