import './vacancy-list.scss';
import {useState} from 'react';
import {Vacancies} from '../../mocks/vacancies';
import VacancyCard from '../vacancy-card/vacancy-card';

function VacancyList() {
  const [currentPage, setCurrentPage] = useState(1);

  return (
    <div className="vacancyListWrapper">
      <div className="vacancyListItem vacancyListItem__list">
        {
          Vacancies.map((vacancy) => {
            return (<VacancyCard vacancy={vacancy}/>);
          })
        }
      </div>
      <div className="vacancyListItem vacancyListItem__pagination">

      </div>
    </div>
  );
}

export default VacancyList;