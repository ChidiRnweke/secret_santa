pub mod schema;
use axum::Json;
use diesel::prelude::*;
use rand::prelude::*;
use serde::{Deserialize, Serialize};

#[derive(Queryable, Selectable, Insertable)]
#[diesel(check_for_backend(diesel::pg::Pg))]
#[diesel(belongs_to(Session))]
#[diesel(table_name = schema::user_assignments)]
struct UserAssignment {
    name: String,
    buys_for: String,
}

#[derive(Deserialize)]
struct CreateUserAssignment {
    users: Vec<String>,
}

#[derive(Queryable, Selectable, Insertable)]
#[diesel(check_for_backend(diesel::pg::Pg))]
#[diesel(table_name = schema::session)]
struct Session {
    id: i32,
}

fn persist_assignment(
    assignment: Vec<UserAssignment>,
    conn: &mut PgConnection,
) -> QueryResult<usize> {
    diesel::insert_into(schema::user_assignments::table)
        .values(&assignment)
        .execute(conn)
}

async fn create_assignment(Json(users): Json<CreateUserAssignment>) {
    let num_users: usize = users.users.len();
    let assignment = (num_users % 2 == 0).then(|| user_list_to_assignments(users.users));
}

fn user_list_to_assignments(users: Vec<String>) -> Vec<UserAssignment> {
    let mut users = users;
    users.shuffle(&mut thread_rng());
    users
        .iter()
        .zip(users.iter().skip(1))
        .map(|(buys_for, buys_from)| UserAssignment {
            buys_for: buys_for.clone(),
            name: buys_from.clone(),
        })
        .collect()
}

fn main() {
    println!("Hello, world!");
}
