import Project from './Project'

import { type Project as ProjectType } from '../models/ProjectsResponse'
import styles from './../style/components/ProjectList.module.css'

interface Props {
  projects: ProjectType[]
  onFavoriteChanged: () => void
}

export default function ProjectList(props: Props): JSX.Element {
  if (props.projects.length === 0) {
    return <></>
  }

  return (
    <div className={styles['project-list']}>
      {props.projects.map((project) => (
        <Project
          project={project}
          key={project.name}
          onFavoriteChanged={() => {
            props.onFavoriteChanged()
          }}
        />
      ))}
    </div>
  )
}
