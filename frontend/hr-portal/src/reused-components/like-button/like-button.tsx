import noLikeIcon from '../../assets/img/vacancy-card/no_like.svg';
import redLikeIcon from '../../assets/img/vacancy-card/no_like_red.svg';
import yesLikeIcon from '../../assets/img/vacancy-card/yes_like.svg';
import whiteLikeIcon from '../../assets/img/vacancy-card/yes_like_white.svg';
import {useEffect, useState} from 'react';
import {Vacancy} from '../../types/vacancy';

type LikeButtonProps = {
  onLike: () => void,
  onDislike: () => void
  liked: boolean
};

export function LikeButton(props: LikeButtonProps) {
  const [icon, setIcon] = useState(noLikeIcon);
  const [liked, setLiked] = useState(props.liked);
  const [hovered, setHovered] = useState(false);

  useEffect(() => {
    let mounted = true;

    if (mounted) {
      setLiked(props.liked);
      //setIcon(props.liked ? yesLikeIcon : noLikeIcon);
      chooseIcon();
    }

    return () => {
      mounted = false;
    };
  }, [props.liked]);

  useEffect(() => {
    let mounted = true;

    if (mounted) {
      chooseIcon();
    }

    return () => {
      mounted = false;
    };
  }, [liked, hovered]);


  const chooseIcon = () => {
    if (liked) {
      setIcon(hovered ? whiteLikeIcon : yesLikeIcon);
    } else {
      setIcon(hovered ? redLikeIcon : noLikeIcon);
    }
  };

  return (
    <button
      type='button'
      className={`navTabs-btnItem__like navTabs-btnItem__like${liked ? '_yes' : ''}`}
      onClick={(evt) => {
        evt.stopPropagation();
        if (!liked) {
          props.onLike();
        }
        else {
          props.onDislike();
        }
      }}
      onMouseEnter={() => {
        setHovered(true);
      }}
      onMouseLeave={() => {
        setHovered(false);
      }}>
      <img
        src={icon}
        alt="likes icon"
      />
    </button>
  );
}