import likesIcon from '../../assets/img/vacancy-card/yes_like.svg';
import {setStateRespondModal, setVacancyByID} from '../../features/vacancy/vacancy-slice';
import {useAppDispatch} from '../../app/hooks';
import VacancyCard from '../vacancy-card/vacancy-card';
import {Vacancy} from '../../types/vacancy';

type ButtonActionVacancyCardProps = {
  vacancy: Vacancy
}


function ButtonActionVacancyCard(props: ButtonActionVacancyCardProps) {
  const {vacancy} = props;
  const dispatch = useAppDispatch();

  const handlerClickRespond = (e: any) => {
    dispatch(setVacancyByID(vacancy));
    e.stopPropagation();
    dispatch(setStateRespondModal(true));
  };

  return (
    <>
      <button className="navTabs-btnItem">
        <img src={likesIcon} alt="likes icon"/>
      </button>
      <button
        className="navTabs-btnItem navTabs-btnItem__respond"
        onClick={handlerClickRespond}
      >
        Откликнуться
      </button>
    </>
  );
}

export default ButtonActionVacancyCard;