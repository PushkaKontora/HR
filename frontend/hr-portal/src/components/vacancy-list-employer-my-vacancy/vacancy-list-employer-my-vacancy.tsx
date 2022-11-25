import VacancyList from '../vacancy-list/vacancy-list';
import {useEffect} from 'react';
import {getVacanciesForEmployer} from '../../service/async-actions/async-actions-vacancy';
import {useAppDispatch, useAppSelector} from '../../app/hooks';

function VacancyListEmployerMyVacancy() {
  const isPublished = useAppSelector((state) => state.vacancy.isPublishedVacancy);
  const idDepartment = useAppSelector((state) => state.general.user?.department.id);
  const offset = useAppSelector((state) => state.vacancy.paramsForGetVacancies.offset);
  const dispatch = useAppDispatch();

  useEffect(() => {
    console.log(1,idDepartment)
    if (idDepartment) {
      console.log('ddd')
      dispatch(getVacanciesForEmployer({isPublished, idDepartment: idDepartment, offset}));
    }
  }, [isPublished,idDepartment]);

  return (
    <VacancyList/>
  );
}

export default VacancyListEmployerMyVacancy;