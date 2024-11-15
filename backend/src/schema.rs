// @generated automatically by Diesel CLI.

diesel::table! {
    session (id) {
        id -> Int4,
        created_at -> Timestamp,
        #[max_length = 255]
        name -> Varchar,
    }
}

diesel::table! {
    user_assignments (id) {
        id -> Int4,
        #[max_length = 255]
        // buys_for -> Varchar,
        #[max_length = 255]
        buys_from -> Varchar,
        created_at -> Timestamp,
        session_id -> Int4,
    }
}

diesel::joinable!(user_assignments -> session (session_id));

diesel::allow_tables_to_appear_in_same_query!(session, user_assignments,);
