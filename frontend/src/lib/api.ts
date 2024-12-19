import createClient from 'openapi-fetch'
import type { paths, components } from './spec.d.ts'

type AssignmentInput = components['schemas']['AssignmentInput']
export type AssignmentResponse = {
  assignment_name: string
  assignments: UserAssignment[]
}

type UserAssignment = components['schemas']['UserAssignment']

class SantaService {
  private client: ReturnType<typeof createClient<paths>>
  public constructor() {
    this.client = createClient<paths>({
      baseUrl: '/api',
    })
  }

  async makeAssignment(users: AssignmentInput): Promise<AssignmentResponse> {
    const { data, error } = await this.client.POST('/assignments', {
      body: users,
    })

    if (error) {
      throw new Error(JSON.stringify(error))
    }
    return data
  }

  async getAssignment(
    assignment_id: string,
    buy_for: string,
  ): Promise<UserAssignment> {
    const { data, error } = await this.client.GET(
      '/assignments/{assignment_id}/{buy_for}',
      { params: { path: { assignment_id, buy_for } } },
    )

    if (error) {
      throw new Error(JSON.stringify(error))
    }
    return data
  }
}
export const santaService = new SantaService()
