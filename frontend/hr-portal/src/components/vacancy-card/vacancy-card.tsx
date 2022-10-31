import {Vacancy} from '../../types/vacancy';

type VacancyCard = {
  vacancy: Vacancy
}

function VacancyCard(props: VacancyCard) {
  const {vacancy} = props;
  return (
    <div className='vacancyCardWrapper'>
      <div className="vacancyCardItem">
        <div className="vacancyCardInfo vacancyCardInfo__title">
          {vacancy.name}
        </div>
        <div className="vacancyCardInfo vacancyCardInfo__description">
          {vacancy.description}
        </div>
        <div className="vacancyCardInfo vacancyCardInfo__tabs">

        </div>
      </div>
      <div className="vacancyCardItem">

      </div>
    </div>
  );
}

export default VacancyCard;