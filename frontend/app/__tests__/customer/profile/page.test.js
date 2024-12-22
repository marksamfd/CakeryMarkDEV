import '@testing-library/jest-dom';
import { render } from '@testing-library/react';
import ProfilePage from '@/app/(customer)/profile/page';

describe('ProfilePage Component', () => {
  it('renders the profile title', () => {
    const { container } = render(<ProfilePage />);
    expect(container).toMatchSnapshot();
  });

  it('renders the edit profile button', () => {
    const { container } = render(<ProfilePage />);
    expect(container).toMatchSnapshot();
  });
});