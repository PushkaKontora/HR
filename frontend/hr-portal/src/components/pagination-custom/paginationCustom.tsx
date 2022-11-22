import {useEffect, useLayoutEffect, useRef, useState} from 'react';

import {Pagination, PaginationItem} from '@mui/material';

import './pagination-custom.scss';
import arrowLeftPagination from '../../assets/img/job-seach/ArrowLeft-pagination.svg';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {setOffsetParam} from '../../features/vacancy/vacancy-slice';
import {getVacancies, getVacanciesForEmployer} from '../../service/async-actions/async-actions-vacancy';


function PaginationCustom() {
  const currentPage =  useAppSelector((state) => state.vacancy.currentPage);
  const maxPageCount = useAppSelector((state) => state.vacancy.maxPagesVacancies);
  const vacancies = useAppSelector((state) => state.vacancy.vacancies);
  const isGetVacanciesEmployer = useAppSelector((state) => state.vacancy.vacancies);
  const departmentId = useAppSelector((state) => state.general?.user?.department.id);
  const offset = useAppSelector((state) => state.vacancy.paramsForGetVacancies.offset);
  const isPublished = useAppSelector((state) => state.vacancy.isPublishedVacancy);
  const dispatch = useAppDispatch();
  const firstUpdate = useRef(true);

  useLayoutEffect(() => {
    if (firstUpdate.current) {
      firstUpdate.current = false;
      return;
    }
  });
  useEffect(() => {
    if(isGetVacanciesEmployer){
      if (departmentId) {
        dispatch(getVacanciesForEmployer({isPublished, idDepartment: departmentId, offset}));
      }
    }else{
      dispatch(getVacancies());
    }
  }, [currentPage]);


  return (
    <div className="vacancyListPagination">
      {
        vacancies.items.length !== 0 && (
          <Pagination
            count={maxPageCount}
            page={currentPage}
            onChange={(_, num) => dispatch(setOffsetParam(num))}
            variant="outlined"
            shape="rounded"

            renderItem={(item) => (
              <PaginationItem
                slots={{
                  previous: () => (<div><img src={arrowLeftPagination} alt="arrowLeftPagination"/></div>),
                  next: () => (<div><img src={arrowLeftPagination} alt="arrowLeftPagination" className="arrow-right"/></div>)
                }}
                {...item}
              />
            )}
          />
        )
      }
      {/*{maxPage !== 0 && (*/}
      {/*  <div className="vacancyListItem vacancyListItem__pagination">*/}
      {/*    <div className="paginationItem">*/}
      {/*      <img src={ArrowPagination} alt="arrow pagination-custom"/>*/}
      {/*    </div>*/}
      {/*    {*/}
      {/*      maxPage < 6 ? (*/}
      {/*        [...Array(maxPage)].map((item, index) => (*/}
      {/*          <div className={cl('paginationItem', {'activePage': index + 1 === currentPage})} key={index}>*/}
      {/*            {index + 1}*/}
      {/*          </div>*/}
      {/*        ))*/}
      {/*      ) : (*/}
      {/*        [...Array(maxPage)].map((item, index) => (*/}
      {/*          <div className={cl('paginationItem', {'activePage': index + 1 === currentPage})} key={index}>*/}
      {/*            {index + 1}*/}
      {/*          </div>*/}
      {/*        ))*/}
      {/*      )*/}
      {/*    }*/}
      {/*    <div className="paginationItem">*/}
      {/*      <img src={ArrowPagination} alt="arrow pagination-custom" className="arrow-right"/>*/}
      {/*    </div>*/}
      {/*  </div>*/}
      {/*)}*/}
    </div>
  );
}

export default PaginationCustom;

//todo: убрать омментарии созания своей пагинации - оставлено на случай, если что-то пойдет не так с запросами