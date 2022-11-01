import {Vacancy} from '../../types/vacancy';
import moneyIcon from '../../assets/img/vacancy-card/money.svg';
import experienceIcon from '../../assets/img/vacancy-card/experience.svg';
import likesIcon from '../../assets/img/vacancy-card/yes_like.svg';
import './vacancy-card.scss';
import {ExpectedExperienceNameString} from '../../const';

type VacancyCard = {
  vacancy: Vacancy
}

function VacancyCard(props: VacancyCard) {
  const {vacancy} = props;

  const vacancyExperience = ExpectedExperienceNameString[vacancy.expected_experience as keyof typeof ExpectedExperienceNameString];
  return (
    <div className="vacancyCardWrapper">
      <div className="vacancyCardItem vacancyCardItem__content">
        <div className="vacancyCardInfo vacancyCardInfo__title">
          {vacancy.name}
        </div>
        <div className="vacancyCardInfo vacancyCardInfo__description">
          {vacancy.description}
        </div>
        <div className="vacancyCardInfo vacancyCardInfo__tabs">
          <div className="tabsItem">
            <div className="tabs-image">
              <img src={experienceIcon} alt="money icon"/>
            </div>
            <div className="tabs-text">
              {vacancyExperience}
            </div>
          </div>
          {(vacancy.salary_to || vacancy.salary_from) &&
          (
            <div className="tabsItem">
              <div className="tabs-image">
                <img src={moneyIcon} alt="experience icon"/>
              </div>
              <div className="tabs-text">

              </div>
            </div>
          )
          }
        </div>
      </div>
      <div className="vacancyCardItem vacancyCardItem__action">
        <div className="actionItem actionItem__department">
          <span>{vacancy.department.name}</span> {vacancy.department.leader.name} {vacancy.department.leader.surname}
        </div>
        <div className="actionItem actionItem__navTabs">
          <button className="navTabs-btnItem">
            <img src={likesIcon} alt="likes icon"/>
          </button>
          <button className="navTabs-btnItem navTabs-btnItem__respond">
            Откликнуться
          </button>
        </div>
      </div>
    </div>
  );
}

export default VacancyCard;

//TODO: сделать лайк закрашенным, если выбран в избранное у пользователя