import likesIcon from '../../assets/img/vacancy-card/yes_like.svg';
import {setStateUnpublishedVacancy, setStateRespondModal, setVacancyByID, setStateEditVacancy} from '../../features/vacancy/vacancy-slice';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {Vacancy} from '../../types/vacancy';
import {ButtonVacancyCard} from '../../const';

type ButtonActionVacancyCardProps = {
  vacancy: Vacancy
}

function ButtonActionVacancyCard(props: ButtonActionVacancyCardProps) {
  const {vacancy} = props;
  const buttonView = useAppSelector((state) => state.page.buttonVacancyCard);
  const dispatch = useAppDispatch();

  const handlerClickRespond = (e: any) => {
    dispatch(setVacancyByID(vacancy));
    e.stopPropagation();
    dispatch(setStateRespondModal(true));
  };

  const handlerClickUnpublishVacancy = (e: any) => {
    dispatch(setVacancyByID(vacancy));
    e.stopPropagation();
    dispatch(setStateUnpublishedVacancy(true));
  };

  const handlerClickEditVacancy = (e: any) => {
    dispatch(setVacancyByID(vacancy));
    e.stopPropagation();
    dispatch(setStateEditVacancy(true));
  };

  return (
    <>
      {buttonView === ButtonVacancyCard.vacancies
      && (<>
        <button className="navTabs-btnItem">
          <img src={likesIcon} alt="likes icon"/>
        </button>
        <button
          className="navTabs-btnItem navTabs-btnItem__respond"
          onClick={handlerClickRespond}
        >
          Откликнуться
        </button>
      </>)
      }
      {buttonView === ButtonVacancyCard.empMyVacancy
      && (<>
        <button
          className="navTabs-btnItem navTabs-btnItem__respond"
          onClick={handlerClickUnpublishVacancy}
        >
          Снять с публикации
        </button>
        <button
          className="navTabs-btnItem navTabs-btnItem__respond"
          onClick={handlerClickEditVacancy}
        >
          Редактировать
        </button>
      </>)
      }
    </>
  );
}

export default ButtonActionVacancyCard;