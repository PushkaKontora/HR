import {Vacancy} from '../../types/vacancy';
import moneyIcon from '../../assets/img/vacancy-card/money.svg';
import experienceIcon from '../../assets/img/vacancy-card/experience.svg';
import likesIcon from '../../assets/img/vacancy-card/no_like.svg';
import './vacancy-card.scss';
import {ExpectedExperienceNameString} from '../../const';
import {useAppDispatch} from '../../app/hooks';
import {setStateRespondModal, setVacancyByID} from '../../features/vacancy/vacancy-slice';
import {useNavigate} from 'react-router-dom';
import {NoAuthRoutes} from '../../const/app-routes';
import moneyRUSIcon from '../../assets/img/job-seach/₽.svg';
import {LikeButton} from '../../reused-components/like-button/like-button';
import {addToVacancyWishlist} from '../../service/async-actions/async-actions-vacancy';
import {toast} from 'react-toastify';

type VacancyCard = {
  vacancy: Vacancy
}

function VacancyCard(props: VacancyCard) {
  const {vacancy} = props;
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  const vacancyExperience = ExpectedExperienceNameString[vacancy.expected_experience as keyof typeof ExpectedExperienceNameString];
  const handleClickVacancyCard = () => {
    dispatch(setVacancyByID(vacancy));
    navigate(`${NoAuthRoutes.Vacancy}/${vacancy.id}`);
  };

  const handlerClickRespond = (e: any) => {
    dispatch(setVacancyByID(vacancy));
    e.stopPropagation();
    dispatch(setStateRespondModal(true));
  };

  const like = () => {
    if (vacancy) {
      dispatch(addToVacancyWishlist(vacancy.id))
        .then(() => {
          toast.success('Вакансия добавлена в избранное');
        });
    }
  };

  return (
    <div className="vacancyCardWrapper" onClick={handleClickVacancyCard}>
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
              {
                vacancy?.salary_to !== null && vacancy?.salary_from === null &&
                (
                  <>
                    <div className="tabs-text">до {vacancy?.salary_to}</div>
                    <div className="tabs-image-rus">
                      <img src={moneyRUSIcon} alt="money rus icon"/>
                    </div>
                  </>
                )
              }
              {
                vacancy?.salary_to === null && vacancy?.salary_from !== null &&
                (
                  <>
                    <div className="tabs-text">от {vacancy?.salary_from}</div>
                    <div className="tabs-image-rus">
                      <img src={moneyRUSIcon} alt="money rus icon"/>
                    </div>
                  </>
                )
              }
              {
                vacancy?.salary_to !== null && vacancy?.salary_from !== null &&
                (<div className="tabs-text">
                  <div className="tabs-flex">
                    <div className="text">от {vacancy?.salary_from}</div>
                    <div className="tabs-image-rus">
                      <img src={moneyRUSIcon} alt="money rus icon"/>
                    </div>
                  </div>
                  <div className="tabs-flex">
                    <div className="text">до {vacancy?.salary_to}</div>
                    <div className="tabs-image-rus">
                      <img src={moneyRUSIcon} alt="money rus icon"/>
                    </div>
                  </div>
                </div>)
              }
            </div>
          )
          }
        </div>
      </div>
      <div className="resumeCardItem vacancyCardItem__action">
        <div className="actionItem actionItem__department">
          <span>{vacancy.department.name}</span> {vacancy.department.leader.name} {vacancy.department.leader.surname}
        </div>
        <div className="actionItem navTabs">
          <LikeButton onLike={like}/>
          <button
            className="navTabs-btnItem navTabs-btnItem__respond"
            onClick={handlerClickRespond}
          >
            Откликнуться
          </button>
        </div>
      </div>
    </div>
  );
}

export default VacancyCard;

//TODO: сделать лайк закрашенным, если выбран в избранное у пользователя