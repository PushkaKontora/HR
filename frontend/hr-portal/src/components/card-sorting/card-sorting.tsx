import {useEffect, useRef, useState} from 'react';

import './card-sorting.scss';
import arrowIcon from '../../assets/img/job-seach/Arrow-select.svg';
import {ExpectedExperience, SortingVacancyTypes} from '../../const';
import {getVacancies} from '../../service/async-actions/async-actions-vacancy';
import {useAppDispatch} from '../../app/hooks';

const SelectFilterCard = {
  [SortingVacancyTypes.BY_NAME]: 'По умолчанию',
  [SortingVacancyTypes.PUBLISHED_DATE]: 'По дате',
  [SortingVacancyTypes.SALARY_DESC]: 'По убыванию зарплаты',
  [SortingVacancyTypes.SALARY_ASC]: 'По возрастанию зарплаты'
};

function CardSorting() {
  const [selectFilterCard, setSelectFilterCard] = useState('По умолчанию');
  const [isOpenFilterCard, setIsOpenFilterCard] = useState(false);
  const refModal = useRef(null);
  const dispatch = useAppDispatch();

  useEffect(() => {
    const child = document.getElementById('child');
    const parent = document.getElementById('parent');
    if (child && parent) {
      const cWidth = child.offsetWidth;
      const pWidth = parent.offsetWidth;
      (cWidth) > pWidth ? child.style.width = (cWidth) + 'px' : child.style.width = (pWidth) + 'px';
    }
  },);

  useEffect(() => {
    setIsOpenFilterCard(false);
  }, [selectFilterCard]);

  // useEffect(() => {
  //   const handleClickOutside = (e: any) => {
  //     if (!refModal.current) return;
  //     if (refModal && !refModal.current.contains(e.target)) {
  //       setIsOpenFilterCard(false);
  //     }
  //   };
  //   document.addEventListener('onmousedown', (e) => handleClickOutside(e));
  //   return () => document.removeEventListener('onmousedown', (e) => handleClickOutside(e));
  // }, []);

  const onToggleSelect = () => {
    setIsOpenFilterCard(!isOpenFilterCard);
  };

  function onHandlerSelectAnotherTypeSort(element: string) {
    setSelectFilterCard(element);
    const experienceData = Object.entries(SelectFilterCard).filter(e => e[1] === element);
    dispatch(getVacancies({sortBy: experienceData[0][0] as SortingVacancyTypes, offset: 1}));
  }

  return (
    <div className="variantsSorted" ref={refModal}>
      <button
        id="parent"
        onClick={onToggleSelect}
        className={isOpenFilterCard ? 'variantSorted-select-btn variantSorted-select-btn__active' : 'variantSorted-select-btn'}
      >
        <div className="btn-text">
          {selectFilterCard}
        </div>
        <div className={isOpenFilterCard ? 'btn-wrapper-array-img' : 'btn-wrapper-array-img__closed'}>
          <img src={arrowIcon} alt="Arrow-select"/>
        </div>
      </button>
      {isOpenFilterCard && (
        <div className="variantSorted-option-wrapper">
          <ul id="child">
            {
              Object.values(SelectFilterCard).map((element, index) => {
                return (
                  selectFilterCard !== element &&
                  <li key={index} onClick={() => onHandlerSelectAnotherTypeSort(element)} className="variantSorted-element">
                    {element}
                  </li>
                );
              })
            }
          </ul>
        </div>
      )}
    </div>
  );
}

export default CardSorting;

//todo: сделать закрытие сортировке по клику вне области (stopPropagination)