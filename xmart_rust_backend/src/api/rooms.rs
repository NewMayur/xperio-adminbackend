use warp::Filter;

pub fn routes() -> impl Filter<Extract = impl warp::Reply, Error = warp::Rejection> + Clone {
    warp::path("rooms")
        .and(warp::get())
        .map(|| "Rooms endpoint")
}
