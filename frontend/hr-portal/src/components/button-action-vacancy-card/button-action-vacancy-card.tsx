import {setStateUnpublishedVacancy, setStateRespondModal, setVacancyByID, setStatePublishedVacancy, setTypeRequestModalVacancy, setIsOpenEditVacancyModal} from '../../features/vacancy/vacancy-slice';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {Vacancy} from '../../types/vacancy';
import {ButtonVacancyCard, TypeRequestVacancyModal} from '../../const';
import {LikeButton} from '../../reused-components/like-button/like-button';
import {addToVacancyWishlist, deleteFromVacancyWishlist} from '../../service/async-actions/async-actions-vacancy';
import {toast} from 'react-toastify';
import {isFavorite} from '../../utils/favorite';
import {useState} from 'react';

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

  const favoriteVacancies = useAppSelector((state) => state.user.favoriteVacancies);

  const [liked, setLiked] = useState(isFavorite(vacancy, favoriteVacancies));

  const like = () => {
    if (vacancy) {
      dispatch(addToVacancyWishlist(vacancy.id))
        .then(() => {
          toast.success('Вакансия добавлена в избранное');
          setLiked(true);
        });
    }
  };

  const dislike = () => {
    if (vacancy) {
      dispatch(deleteFromVacancyWishlist(vacancy.id))
        .then(() => {
          toast.error('Вакансия удалена из избранного');
          setLiked(false);
        });
    }
  };

  return (
    <>
      {buttonView === ButtonVacancyCard.vacancies
      && (<>
        <LikeButton
          onLike={like}
          onDislike={dislike}
          liked={liked}
        />
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