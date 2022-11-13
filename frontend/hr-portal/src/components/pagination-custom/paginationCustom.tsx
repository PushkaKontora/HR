import {useEffect, useState} from 'react';

import {Pagination, PaginationItem} from '@mui/material';

import './pagination-custom.scss';
import arrowLeftPagination from '../../assets/img/job-seach/ArrowLeft-pagination.svg';


function PaginationCustom() {
  const [vacancyOnPage, setVacancyOnPage] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);

  const [maxPageCount, setMaxPageCount] = useState(15);

  useEffect(() => {
    //запрос на страницы(на контент)
  }, [currentPage]);


  return (
    <div className="vacancyListPagination">
      {
        !!maxPageCount && (
          <Pagination
            count={maxPageCount}
            page={currentPage}
            onChange={(_, num) => setCurrentPage(num)}
            variant="outlined"
            shape="rounded"

            renderItem={(item) => (
              <PaginationItem
                slots={{
                  previous: () => (<div><img src={arrowLeftPagination} alt="arrowLeftPagination"/></div>),
                  next: () => (<div><img src={arrowLeftPagination} alt="arrowLeftPagination" className='arrow-right'/></div>)
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