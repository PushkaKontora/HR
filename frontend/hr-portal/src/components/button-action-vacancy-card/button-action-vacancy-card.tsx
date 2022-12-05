import {setStateUnpublishedVacancy, setStateRespondModal, setVacancyByID, setStatePublishedVacancy, setTypeRequestModalVacancy, setIsOpenEditVacancyModal} from '../../features/vacancy/vacancy-slice';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {Vacancy} from '../../types/vacancy';
import {ButtonVacancyCard, TypeRequestVacancyModal} from '../../const';
import {LikeButton} from '../../reused-components/like-button/like-button';
import {addToVacancyWishlist} from '../../service/async-actions/async-actions-vacancy';
import {toast} from 'react-toastify';

type ButtonActionVacancyCardProps = {
  vacancy: Vacancy
}

function ButtonActionVacancyCard(props: ButtonActionVacancyCardProps) {
  const {vacancy} = props;
  const buttonView = useAppSelector((state) => state.page.buttonVacancyCard);
  const isPublishedVacancy = useAppSelector((state) => state.vacancy.isPublishedVacancy);
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

  const handlerClickPublishVacancy = (e: any) => {
    dispatch(setVacancyByID(vacancy));
    e.stopPropagation();
    dispatch(setStatePublishedVacancy(true));
  };

  const handlerClickEditVacancy = (e: any) => {
    dispatch(setVacancyByID(vacancy));
    e.stopPropagation();
    dispatch(setTypeRequestModalVacancy(TypeRequestVacancyModal.CHANGE));
    dispatch(setIsOpenEditVacancyModal(true));
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
    <>
      {buttonView === ButtonVacancyCard.vacancies
      && (<>
        <LikeButton onLike={like}/>
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
        {isPublishedVacancy
          ? (
            <button
              className="navTabs-btnItem navTabs-btnItem__respond"
              onClick={handlerClickUnpublishVacancy}
            >
              Снять с публикации
            </button>
          ) : (
            <button
              className="navTabs-btnItem navTabs-btnItem__respond"
              onClick={handlerClickPublishVacancy}
            >
              Опубликовать
            </button>
          )}

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