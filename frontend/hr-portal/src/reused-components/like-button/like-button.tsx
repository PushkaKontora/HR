import likesIcon from '../../assets/img/vacancy-card/no_like.svg';

type LikeButtonProps = {
  onLike: () => void,
  //onDislike: () => void,
  //initState: boolean
};

export function LikeButton(props: LikeButtonProps) {
  return (
    <button
      type='button'
      className="navTabs-btnItem"
      onClick={(evt) => {
        evt.stopPropagation();
        props.onLike();
      }}>
      <img src={likesIcon} alt="likes icon"/>
    </button>
  );
}