import VacancyCard from '../vacancy-card/vacancy-card';
import PaginationCustom from '../pagination-custom/paginationCustom';
import {useAppSelector} from '../../app/hooks';

function VacancyList() {
  const vacancies = useAppSelector((state) => state.vacancy.vacancies);

  return (
    <div className="vacancyListWrapper">
      <div className="vacancyListItem vacancyListItem__list">
        {
          vacancies.items.map((vacancy) => {
            return (<VacancyCard key={vacancy.id} vacancy={vacancy}/>);
          })
        }
      </div>
      <PaginationCustom/>
    </div>
  );
}

export default VacancyList;