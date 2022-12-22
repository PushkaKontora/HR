import {useEffect, useLayoutEffect, useRef, useState} from 'react';

import {Pagination, PaginationItem} from '@mui/material';

import './pagination-custom.scss';
import arrowLeftPagination from '../../assets/img/job-seach/ArrowLeft-pagination.svg';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {setOffsetParam} from '../../features/vacancy/vacancy-slice';
import {getVacancies, getVacanciesForEmployer} from '../../service/async-actions/async-actions-vacancy';
import {TypeActionPagination} from '../../const';
import {getResumeList} from '../../service/async-actions/async-actions-resume';

type PaginationCustomProps = {
  itemList: any[],
  onChange?: () => void
};

function PaginationCustom(props: PaginationCustomProps) {
  const {itemList} = props;
  const currentPage = useAppSelector((state) => state.vacancy.currentPage);
  const maxPageCount = useAppSelector((state) => state.vacancy.maxPagesItemsForPagination);
  const typeActionPagination = useAppSelector((state) => state.vacancy.typeActionPagination);
  const departmentId = useAppSelector((state) => state.general?.user?.department?.id);
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
    if (typeActionPagination === TypeActionPagination.VACANCY_EMPLOYER) {
      if (departmentId) {
        dispatch(getVacanciesForEmployer({isPublished, idDepartment: departmentId, offset}));
      }
    } else if (typeActionPagination === TypeActionPagination.VACANCY) {
      dispatch(getVacancies());
    } else if (typeActionPagination === TypeActionPagination.RESUME_EMPLOYER) {
      dispatch(getResumeList());
    }
  }, [currentPage]);


  return (
    <div className="vacancyListPagination">
      {
        itemList.length !== 0 && (
          <Pagination
            count={maxPageCount}
            page={currentPage}
            onChange={(_, num) => {
              dispatch(setOffsetParam(num));
              if (props.onChange)
                props.onChange();
            }}
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
    </div>
  );
}

export default PaginationCustom;

//todo: убрать омментарии созания своей пагинации - оставлено на случай, если что-то пойдет не так с запросами