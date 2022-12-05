import VacancyCard from '../vacancy-card/vacancy-card';
import {useEffect, useLayoutEffect, useRef, useState} from 'react';

import './vacancy-list.scss';
import PaginationCustom from '../pagination-custom/paginationCustom';
import {useAppSelector} from '../../app/hooks';
import {getVacancies} from '../../service/async-actions/async-actions-vacancy';
import ModalRespondRequest from '../modal-respond-request/modal-respond-request';
import {Vacancy} from '../../types/vacancy';

type VacancyListProps = {
  vacancies: Vacancy[],
  showPagination: boolean
}

function VacancyList(props: VacancyListProps) {
  //const vacancies = useAppSelector((state) => state.vacancy.vacancies);
  const [vacState, setVacState] = useState(props.vacancies);
  const firstUpdate = useRef(true);
  //const dispatch = useAppDispatch();

  useLayoutEffect(() => {
    if (firstUpdate.current) {
      firstUpdate.current = false;
      return;
    }
  });

  useEffect(() => {
    let mounted = true;

    if (mounted) {
      setVacState(props.vacancies);
    }

    return () => {
      mounted = false;
    };
  }, [props.vacancies]);


  return (
    <>
      <ModalRespondRequest/>
      <div className="vacancyListWrapper">
        <div className="vacancyListItem vacancyListItem__list">
          {
            props.vacancies.map((vacancy) => {
              return (<VacancyCard key={vacancy.id} vacancy={vacancy}/>);
            })
          }
        </div>
        {props.showPagination && <PaginationCustom/>}
      </div>
    </>
  );
}

export default VacancyList;