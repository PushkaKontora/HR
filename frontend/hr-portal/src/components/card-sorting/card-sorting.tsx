import {useEffect, useState} from 'react';

import './card-sorting.scss';
import arrowIcon from '../../assets/img/job-seach/Arrow-select.svg';

enum SelectFilterCard {
  DEFAULT = 'По умолчанию',
  ON_DATE = 'По дате',
  DECREASE_SALARY = 'По убыванию зарплаты',
  INCREASE_SALARY = 'По возрастанию зарплаты'
}

const selectFilterCardVariants = [SelectFilterCard.DEFAULT, SelectFilterCard.ON_DATE, SelectFilterCard.DECREASE_SALARY, SelectFilterCard.INCREASE_SALARY];


function CardSorting() {
  const [selectFilterCard, setSelectFilterCard] = useState(SelectFilterCard.DEFAULT);

  const [isOpenFilterCard, setIsOpenFilterCard] = useState(false);

  useEffect(() => {
    const child = document.getElementById('child');
    if (child) {
      child.style.width = 280 + 'px';
      //(cWidth + 25) > pWidth ? child.style.width = (cWidth) + 'px' : child.style.width = pWidth + 'px';
    }
  },);

  const onToggleSelect = () => {
    setIsOpenFilterCard(!isOpenFilterCard);
  };
  return (
    <div className="variantsSorted">
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
              selectFilterCardVariants.map((element, index) => {
                return (
                  selectFilterCard !== element &&
                  <li key={index} onClick={() => setSelectFilterCard(element)} className="variantSorted-element">
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